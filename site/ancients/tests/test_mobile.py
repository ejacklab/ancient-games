#!/usr/bin/env python3
"""P3 mobile acceptance checks, written from the accepted blueprint and JSON.

Usage: python3 test_mobile.py [--url URL] [--shots DIR]
These checks establish browser behaviour, not source authenticity (R5.2), actual
S25 Ultra behaviour (P4), or deployment isolation (N3).
"""
from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

from markdown_it import MarkdownIt
from playwright.sync_api import sync_playwright


SITE = Path(__file__).resolve().parents[1]
REPO = SITE.parents[1]
PERSONS = json.loads((SITE / "content/ancients.json").read_text(encoding="utf-8"))["persons"]
VIEWPORT = {"width": 412, "height": 915}
ANDROID_USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 15; SM-S938B) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36"
)
# Choices and value names come from the Kindle template referenced by P2.
FONT_FAMILIES = {
    "literata": "Literata", "georgia": "Georgia",
    "sans": "system-ui", "hyper": "Atkinson Hyperlegible",
}
SIZES = [14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 32]
THEME_BACKGROUNDS = {
    "white": "rgb(255, 255, 255)", "sepia": "rgb(244, 236, 216)",
    "green": "rgb(204, 232, 207)", "black": "rgb(0, 0, 0)",
}


def require(condition, observed):
    if not condition:
        raise AssertionError(observed)


def letters_digits(text):
    return "".join(character for character in text if character.isalnum())


class RenderedText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, text):
        self.parts.append(text)


def markdown_text(markdown):
    parser = RenderedText()
    parser.feed(MarkdownIt("commonmark", {"html": False, "typographer": True})
                .enable(["table", "strikethrough"]).render(markdown))
    return "".join(parser.parts)


def panel_at(page, index):
    panels = page.locator("section.person")
    count = panels.count()
    require(count == 4, f"person panel count={count}, expected 4")
    return panels.nth(index)


def wait_for_scroll_stop(page):
    # Sample all scrollers, including hidden panels, after snap/restore can start.
    page.evaluate("""async () => {
        await new Promise(resolve => setTimeout(resolve, 500));
        const started = performance.now();
        let previous = null, stable = 0;
        while (performance.now() - started < 6000) {
            const positions = [...document.querySelectorAll('#people, section.person')]
                .flatMap(element => [element.scrollLeft, element.scrollTop]);
            if (previous && positions.length === previous.length &&
                positions.every((value, index) => Math.abs(value - previous[index]) < .25)) {
                stable++;
            } else { stable = 0; }
            if (stable >= 4) return;
            previous = positions;
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        throw new Error('scroll positions did not settle: ' + JSON.stringify(previous));
    }""")


def current_person(page):
    panel_at(page, 0)
    row = page.locator("#people")
    require(row.count() == 1, f"#people count={row.count()}")
    offsets = row.evaluate("""row => {
        const left = row.getBoundingClientRect().left + row.clientLeft;
        return [...document.querySelectorAll('section.person')]
            .map(panel => panel.getBoundingClientRect().left - left);
    }""")
    matches = [index for index, offset in enumerate(offsets) if abs(offset) <= 2]
    require(len(matches) == 1, f"panel left offsets={offsets}, expected one within ±2px")
    index = matches[0]
    position = page.locator("#person-pos").inner_text().strip()
    require(position == f"{index + 1} / 4", f"#person-pos={position!r}, panel={index + 1}")
    return index


def go_to_person(page, index):
    panel_at(page, index)
    button = page.locator(f'#dots button[data-goto="{index}"]')
    require(button.count() == 1, f"dot {index} count={button.count()}")
    button.tap()
    wait_for_scroll_stop(page)
    observed = current_person(page)
    require(observed == index, f"current person={observed + 1}, expected {index + 1}")
    return panel_at(page, index)


def swipe_horizontal(page, forward=True):
    panel_at(page, current_person(page))
    width, height = VIEWPORT["width"], VIEWPORT["height"]
    session = page.context.new_cdp_session(page)
    try:
        session.send("Input.synthesizeScrollGesture", {
            "x": width * (.8 if forward else .2), "y": height * .5,
            "xDistance": width * (-.6 if forward else .6), "yDistance": 0,
            "gestureSourceType": "touch", "preventFling": True, "speed": 600,
        })
    finally:
        session.detach()
    wait_for_scroll_stop(page)


def swipe_vertical(page, down=True):
    panel = panel_at(page, current_person(page))
    bounds = panel.bounding_box()
    require(bounds is not None, f"current panel bounds={bounds!r}")
    top = max(bounds["y"], VIEWPORT["height"] * .2)
    bottom = min(bounds["y"] + bounds["height"], VIEWPORT["height"] * .85)
    require(bottom > top, f"vertical gesture area top={top} bottom={bottom}")
    distance = (bottom - top) * .7
    session = page.context.new_cdp_session(page)
    try:
        session.send("Input.synthesizeScrollGesture", {
            "x": VIEWPORT["width"] * .5,
            "y": bottom if down else top,
            "xDistance": 0, "yDistance": -distance if down else distance,
            "gestureSourceType": "touch", "preventFling": True, "speed": 600,
        })
    finally:
        session.detach()
    wait_for_scroll_stop(page)


def scroll_top(panel):
    return panel.evaluate("element => element.scrollTop")


def require_on_screen(locator):
    require(locator.count() == 1, f"{locator} count={locator.count()}")
    bounds = locator.bounding_box()
    require(locator.is_visible() and bounds is not None, f"{locator} visible=False bounds={bounds}")
    require(bounds["x"] >= -1 and bounds["y"] >= -1
            and bounds["x"] + bounds["width"] <= VIEWPORT["width"] + 1
            and bounds["y"] + bounds["height"] <= VIEWPORT["height"] + 1,
            f"{locator} outside viewport: bounds={bounds}")


def require_header(page, index):
    for selector in ("#person-name", "#person-pos"):
        require_on_screen(page.locator(selector))
    name = page.locator("#person-name").inner_text().strip()
    require(name == PERSONS[index]["name"], f"header name={name!r}, expected {PERSONS[index]['name']!r}")
    require(current_person(page) == index, f"header/panel mismatch for person {index + 1}")


def require_item_numbers(panel, person):
    observed = panel.locator(".item[data-n]").evaluate_all(
        "items => items.map(item => item.getAttribute('data-n'))")
    expected = [str(item["n"]) for item in person["items"]]
    require(observed == expected, f"{person['id']} item numbers={observed}, expected {expected}")


def require_field_text(item, selector, expected, description):
    field = item.locator(selector)
    require(field.count() == 1, f"{description} {selector} count={field.count()}")
    require(field.is_visible(), f"{description} {selector} visible=False")
    observed = field.inner_text().strip()
    require(letters_digits(observed) == letters_digits(expected),
            f"{description} {selector} observed={observed!r}, expected={expected!r}")


def test_R1_1(page):
    panels = page.locator("section.person")
    observed_ids = panels.evaluate_all("panels => panels.map(panel => panel.dataset.person)")
    expected_ids = [person["id"] for person in PERSONS]
    require(observed_ids == expected_ids, f"panel ids={observed_ids}, expected {expected_ids}")
    names = panels.locator(".person-name").all_inner_texts()
    require([name.strip() for name in names] == [person["name"] for person in PERSONS],
            f"panel names={names!r}")
    require(current_person(page) == 0, f"initial person={current_person(page) + 1}")
    return True, "four people in JSON order"


def test_R1_2(page):
    for index, person in enumerate(PERSONS):
        panel = go_to_person(page, index)
        require_field_text(panel, ".person-name", person["name"], person["id"])
        who = panel.locator(".who")
        require(who.count() == 1 and who.is_visible(), f"{person['id']} .who count={who.count()}")
        observed = letters_digits(who.inner_text())
        expected = letters_digits(person["who"]["markdown"])
        require(expected in observed, f"{person['id']} .who observed={who.inner_text()!r}")
        require_item_numbers(panel, person)
        for entry in person["items"]:
            item = panel.locator(f'.item[data-n="{entry["n"]}"]')
            description = f"{person['id']} #{entry['n']}"
            for field in ("rule", "words"):
                require_field_text(item, f".{field}", entry[field], description)
            require_field_text(item, ".kind", entry["kind_tag"], description)
            for field in ("source", "label"):
                require_field_text(item, f".{field}", markdown_text(entry[field]), description)
    return True, "all 76 items, names, biographies, sources and labels match JSON"


def test_R1_3(page):
    for index, person in enumerate(PERSONS):
        panel = go_to_person(page, index)
        require_item_numbers(panel, person)
        kinds = panel.locator(".kinds")
        require_on_screen(kinds)
        text = kinds.inner_text().strip()
        matches = re.findall(r"(\d+)\s+(mindsets?|decision rules?|algorithms?)\b", text)
        observed = {kind.removesuffix("s"): int(count) for count, kind in matches}
        expected = Counter(entry["kind_tag"] for entry in person["items"])
        require(len(matches) == len(observed) and bool(matches)
                and all(observed.get(kind) == count for kind, count in expected.items())
                and all(count == expected.get(kind, 0) for kind, count in observed.items()),
                f"{person['id']} kind summary={text!r}, expected={dict(expected)}")
        for entry in person["items"]:
            tag = panel.locator(f'.item[data-n="{entry["n"]}"] .kind')
            require(tag.count() == 1 and tag.is_visible(),
                    f"{person['id']} #{entry['n']} kind visible={tag.count() == 1 and tag.is_visible()}")
            observed_tag = tag.inner_text().strip()
            require(observed_tag == entry["kind_tag"],
                    f"{person['id']} #{entry['n']} kind={observed_tag!r}, expected={entry['kind_tag']!r}")
    return True, "visible kind tags, kind counts and ranked order match JSON"


def test_R2_1(page):
    require(current_person(page) == 0, f"initial person={current_person(page) + 1}")
    swipe_horizontal(page, forward=False)
    require(current_person(page) == 0, f"right swipe at first person={current_person(page) + 1}")
    for index in (1, 2, 3):
        swipe_horizontal(page)
        require(current_person(page) == index, f"forward swipe person={current_person(page) + 1}, expected {index + 1}")
    swipe_horizontal(page)
    require(current_person(page) == 3, f"left swipe at last person={current_person(page) + 1}")
    for index in (2, 1, 0):
        swipe_horizontal(page, forward=False)
        require(current_person(page) == index, f"reverse swipe person={current_person(page) + 1}, expected {index + 1}")
    return True, "touch swipes snap both ways and stop at both ends"


def test_R2_2(page):
    for index in range(4):
        go_to_person(page, index)
        require_header(page, index)
        swipe_vertical(page)
        require_header(page, index)
    return True, "current name and n / 4 stay on screen while reading each person"


def test_R2_3(page):
    dots = page.locator("#dots button[data-goto]")
    observed = dots.evaluate_all("buttons => buttons.map(button => button.dataset.goto)")
    require(observed == ["0", "1", "2", "3"], f"dot values={observed}")
    for index in (3, 1, 2, 0):
        go_to_person(page, index)
    return True, "all four dots jump to their person"


def test_R3_1(page):
    for index in range(4):
        panel = go_to_person(page, index)
        before = scroll_top(panel)
        swipe_vertical(page)
        after = scroll_top(panel)
        require(after > before, f"person {index + 1} down scrollTop before={before} after={after}")
        require(current_person(page) == index, f"vertical swipe changed person to {current_person(page) + 1}")
        swipe_vertical(page, down=False)
        restored = scroll_top(panel)
        require(restored < after, f"person {index + 1} up scrollTop before={after} after={restored}")
        require(current_person(page) == index, f"up swipe changed person to {current_person(page) + 1}")
    return True, "vertical touch scroll moves text both ways without changing people"


def test_R3_2(page):
    panel = go_to_person(page, 0)
    swipe_vertical(page)
    saved = scroll_top(panel)
    require(saved > 0, f"person 1 saved scrollTop={saved}")
    swipe_horizontal(page)
    require(current_person(page) == 1, f"after swipe current person={current_person(page) + 1}")
    swipe_horizontal(page, forward=False)
    require(current_person(page) == 0, f"after return current person={current_person(page) + 1}")
    restored = scroll_top(panel)
    require(restored == saved, f"person 1 saved scrollTop={saved}, restored={restored}")
    return True, f"person 1 scrollTop preserved at {restored:.1f}px"


def open_menu(page):
    button = page.locator("#aa")
    require_on_screen(button)
    require(button.inner_text().strip() == "Aa", f"#aa text={button.inner_text()!r}")
    menu = page.locator("#menu")
    if not menu.is_visible():
        button.tap()
    require(menu.count() == 1 and menu.is_visible(), f"#menu count={menu.count()} visible={menu.is_visible()}")
    return menu


def choose_setting(page, setting, value):
    menu = open_menu(page)
    choice = menu.locator(f'[data-setting="{setting}"][data-value="{value}"]')
    require(choice.count() == 1, f"menu {setting}={value} count={choice.count()}")
    require(choice.evaluate("element => element.tagName") == "BUTTON",
            f"menu {setting}={value} element is not a button")
    choice.tap()
    # Includes the template's background transition and any layout settling.
    wait_for_scroll_stop(page)


def close_menu(page):
    menu = page.locator("#menu")
    if menu.is_visible():
        # P2 specifies a Done button; Aa is only contracted to open the menu.
        done = menu.locator("button").filter(has_text=re.compile(r"^Done$"))
        require(done.count() == 1, f"menu Done button count={done.count()}")
        done.tap()
        require(not menu.is_visible(), "#menu remains visible after Done")


def reading_style(page):
    return panel_at(page, 0).locator(".who").evaluate("""element => {
        const style = getComputedStyle(element);
        const panel = getComputedStyle(element.closest('section.person'));
        let background = 'rgba(0, 0, 0, 0)';
        for (let parent = element; parent; parent = parent.parentElement) {
            const colour = getComputedStyle(parent).backgroundColor;
            if (colour !== 'rgba(0, 0, 0, 0)' && colour !== 'transparent') {
                background = colour; break;
            }
        }
        return {font: style.fontFamily, size: parseFloat(style.fontSize),
            leading: style.lineHeight, margin: panel.paddingLeft,
            align: style.textAlign, background};
    }""")


def test_R4_1(page):
    panel_at(page, 0)
    choices = {
        "font": list(FONT_FAMILIES), "size": [str(size) for size in SIZES],
        "leading": ["compact", "normal", "loose"],
        "margin": ["narrow", "normal", "wide"], "align": ["justify", "left"],
        "theme": list(THEME_BACKGROUNDS),
    }
    properties = {"font": "font", "size": "size", "leading": "leading",
                  "margin": "margin", "align": "align", "theme": "background"}
    for setting, values in choices.items():
        observed_values = open_menu(page).locator(f'[data-setting="{setting}"]').evaluate_all(
            "buttons => buttons.map(button => button.dataset.value)")
        require(set(values).issubset(observed_values),
                f"{setting} menu values={observed_values}, expected={values}")
        last_value = None
        for value in values:
            before = reading_style(page)[properties[setting]]
            choose_setting(page, setting, value)
            observed = reading_style(page)[properties[setting]]
            if last_value is not None:
                require(observed != before, f"{setting} {last_value}→{value}: computed {properties[setting]} stayed {observed!r}")
            if setting == "font":
                require(FONT_FAMILIES[value].lower() in observed.lower(), f"font={value} computed font-family={observed!r}")
            elif setting == "size":
                require(abs(observed - int(value)) < .1, f"size={value} computed font-size={observed}")
            elif setting == "align":
                require(observed == value, f"align={value} computed text-align={observed!r}")
            elif setting == "theme":
                require(observed == THEME_BACKGROUNDS[value], f"theme={value} computed background={observed!r}")
            last_value = value
    return True, "every Kindle font, size, spacing, margin, alignment and theme takes effect"


def test_R4_2(page):
    first = panel_at(page, 0)
    require(reading_style(page)["background"] == THEME_BACKGROUNDS["sepia"],
            f"initial background={reading_style(page)['background']!r}, expected sepia")
    choose_setting(page, "theme", "black")
    require(reading_style(page)["background"] == THEME_BACKGROUNDS["black"],
            f"selected black background={reading_style(page)['background']!r}")
    close_menu(page)
    swipe_vertical(page)
    saved_first = scroll_top(first)
    require(saved_first > 0, f"person 1 saved scrollTop={saved_first}")
    third = go_to_person(page, 2)
    swipe_vertical(page)
    saved_third = scroll_top(third)
    require(saved_third > 0, f"person 3 saved scrollTop={saved_third}")
    page.reload(wait_until="load")
    page.evaluate("() => document.fonts.ready.then(() => true)")
    wait_for_scroll_stop(page)
    require(reading_style(page)["background"] == THEME_BACKGROUNDS["black"],
            f"reloaded background={reading_style(page)['background']!r}")
    observed_person = current_person(page)
    require(observed_person == 2, f"reloaded person={observed_person + 1}, expected 3")
    restored_third = scroll_top(panel_at(page, 2))
    restored_first = scroll_top(panel_at(page, 0))
    require(abs(restored_third - saved_third) <= 40,
            f"person 3 saved scrollTop={saved_third}, restored={restored_third}, tolerance=40px")
    require(abs(restored_first - saved_first) <= 40,
            f"person 1 saved scrollTop={saved_first}, restored={restored_first}, tolerance=40px")
    return True, f"black theme, person 3 and scroll places restored ({restored_third:.1f}px)"


def test_R4_3(page):
    for index in range(4):
        panel = go_to_person(page, index)
        dimensions = panel.evaluate("element => ({scrollWidth: element.scrollWidth, clientWidth: element.clientWidth})")
        require(dimensions["scrollWidth"] <= dimensions["clientWidth"] + 1,
                f"person {index + 1} dimensions={dimensions}, tolerance=1px")
    return True, "all four panels have scrollWidth <= clientWidth + 1"


def read_percent(panel):
    footer = panel.locator(".pct")
    require_on_screen(footer)
    text = footer.inner_text().strip()
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*%", text)
    require(match is not None, f"footer text={text!r}, expected a percentage")
    value = float(match.group(1))
    require(0 <= value <= 100, f"footer percentage={value}")
    return value


def test_R4_4(page):
    for index in range(4):
        panel = go_to_person(page, index)
        before = read_percent(panel)
        swipe_vertical(page)
        after = read_percent(panel)
        require(after > before, f"person {index + 1} footer before={before}% after={after}% scrollTop={scroll_top(panel)}")
        # Endpoint check avoids inventing a rounding rule for intermediate % read.
        panel.evaluate("element => { element.scrollTop = element.scrollHeight; }")
        wait_for_scroll_stop(page)
        at_end = read_percent(panel)
        require(at_end == 100, f"person {index + 1} footer at end={at_end}%")
    return True, "each visible footer advances with reading and reaches 100%"


def test_R5_1(page):
    for index, person in enumerate(PERSONS):
        panel = go_to_person(page, index)
        require_item_numbers(panel, person)
        for entry in person["items"]:
            item = panel.locator(f'.item[data-n="{entry["n"]}"]')
            require_field_text(item, ".words", entry["words"], f"{person['id']} #{entry['n']}")
    return True, "all 76 quotations match JSON after letters/digits/CJK normalization"


def test_N2(page, requests, cookie_headers):
    # A blank or unloaded page cannot establish the ancients page's privacy.
    panel_at(page, 0)
    require(page.locator("#people").count() == 1, f"#people count={page.locator('#people').count()}")
    # the document itself is the one file, not a request the page makes (needed when --url is the live address)
    # allowed: Google Fonts, and Cloudflare Web Analytics that the ejai.ai zone injects (EJ, decisions.md D1)
    own = urlsplit(page.url).hostname

    def allowed(url):
        u = urlsplit(url)
        return (u.scheme == "file" or url == page.url
                or u.hostname in {"fonts.googleapis.com", "fonts.gstatic.com", "static.cloudflareinsights.com"}
                or (u.hostname == own and u.path == "/cdn-cgi/rum"))
    forbidden = [url for url in requests if not allowed(url)]
    require(not forbidden, f"forbidden requests={forbidden!r}")
    cookie = page.evaluate("() => document.cookie")
    require(cookie == "", f"document.cookie={cookie!r}")
    require(not cookie_headers, f"Set-Cookie responses={cookie_headers!r}")
    return True, f"{len(requests)} requests recorded; allowed hosts only; no cookies"


TESTS = [
    ("R1.1", test_R1_1), ("R1.2", test_R1_2), ("R1.3", test_R1_3),
    ("R2.1", test_R2_1), ("R2.2", test_R2_2), ("R2.3", test_R2_3),
    ("R3.1", test_R3_1), ("R3.2", test_R3_2),
    ("R4.1", test_R4_1), ("R4.2", test_R4_2), ("R4.3", test_R4_3),
    ("R4.4", test_R4_4), ("R5.1", test_R5_1), ("N2", test_N2),
]


def print_result(criterion, passed, note):
    print(f"{'PASS' if passed else 'FAIL'} {criterion} {' '.join(str(note).split())}", flush=True)


def new_mobile_page(browser, url, requests, cookie_headers):
    context = browser.new_context(
        viewport=VIEWPORT, device_scale_factor=3.5, is_mobile=True,
        has_touch=True, user_agent=ANDROID_USER_AGENT,
    )
    context.on("request", lambda request: requests.append(request.url))

    def record_cookie_header(response):
        value = response.header_value("set-cookie")
        if value is not None:
            cookie_headers.append((response.url, value))

    context.on("response", record_cookie_header)
    page = context.new_page()
    page.set_default_timeout(4000)
    page.set_default_navigation_timeout(30000)
    try:
        page.goto(url, wait_until="load")
        page.evaluate("() => document.fonts.ready.then(() => true)")
        wait_for_scroll_stop(page)
    except Exception:
        context.close()
        raise
    return context, page


def save_screenshots(browser, url, shots, requests, cookie_headers):
    context, page = new_mobile_page(browser, url, requests, cookie_headers)
    try:
        shots.mkdir(parents=True, exist_ok=True)
        for index in range(4):
            go_to_person(page, index)
            page.screenshot(path=str(shots / f"person-{index + 1}.png"))
        open_menu(page)
        page.screenshot(path=str(shots / "menu.png"))
    finally:
        context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=(SITE / "dist/index.html").as_uri())
    parser.add_argument("--shots", type=Path, default=REPO / "runs/20261013-ancients-page/shots")
    arguments = parser.parse_args()
    results = []
    requests, cookie_headers = [], []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                for criterion, test in TESTS:
                    context = None
                    try:
                        context, page = new_mobile_page(browser, arguments.url, requests, cookie_headers)
                        if criterion == "N2":
                            passed, note = test(page, requests, cookie_headers)
                        else:
                            passed, note = test(page)
                        if criterion == "R2.3" and passed:
                            save_screenshots(browser, arguments.url, arguments.shots, requests, cookie_headers)
                    except Exception as error:
                        passed, note = False, f"{type(error).__name__}: {error}"
                    finally:
                        if context is not None:
                            context.close()
                    results.append(passed)
                    print_result(criterion, passed, note)
            finally:
                browser.close()
    except Exception as error:
        # Launch failure is infrastructure evidence, never a claimed red baseline.
        lines = str(error).splitlines()
        headline = lines[0] if lines else str(error)
        fatal = next((line.strip() for line in lines if "FATAL:" in line), "")
        launch_note = f"browser unavailable: {type(error).__name__}: {headline} {fatal}"
        for criterion, _ in TESTS[len(results):]:
            results.append(False)
            print_result(criterion, False, launch_note)
    passed_count = sum(results)
    print(f"SUMMARY {passed_count}/{len(TESTS)}", flush=True)
    return 0 if passed_count == len(TESTS) else 1


if __name__ == "__main__":
    sys.exit(main())
