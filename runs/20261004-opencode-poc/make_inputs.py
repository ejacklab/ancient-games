"""Inputs for the opencode / MiniMax-M3.1-Flash-Preview POC.

Every POC gets an input that can be checked mechanically, so "amazing at" is a measured claim and not an
impression. Run from anywhere: `python3 make_inputs.py`.
"""
import pathlib
import random
import subprocess
import sys

HERE = pathlib.Path(__file__).parent


def p2_long_context() -> int:
    """A ~200k-token record file with three needles at 5%, 50% and 95% depth.

    Long-context claims are cheap to make and cheap to falsify: put the answers at both ends and the middle,
    then ask for all three at once.
    """
    rng = random.Random(20261004)
    # No /usr/share/dict/words on this host, so the filler is synthesized. It only has to be long, varied and
    # free of anything resembling a needle.
    onsets = ["ka", "mor", "tel", "vin", "sar", "lun", "dap", "fen", "gor", "hul", "ith", "jem", "nor", "pex"]
    codas = ["a", "en", "is", "or", "um", "ath", "el", "un", "ir", "os"]
    words = [o + c for o in onsets for c in codas]
    needles = {"ALPHA": 481207, "BETA": 739164, "GAMMA": 205938}
    # ~800 KB of filler is roughly 200k tokens.
    total_chars, chunk = 800_000, 90
    target_positions = {int(total_chars * f): name for f, name in ((0.05, "ALPHA"), (0.5, "BETA"), (0.95, "GAMMA"))}

    out, written, name_at = [], 0, None
    while written < total_chars:
        for pos, name in sorted(target_positions.items()):
            if name_at != name and written >= pos:
                out.append(f"RECORD {name}: the access code for {name} is {needles[name]}.\n")
                written += 60
                name_at = name
        line = " ".join(rng.choice(words) for _ in range(chunk))
        out.append(line + "\n")
        written += len(line) + 1
    body = "".join(out)
    (HERE / "p2_records.txt").write_text(body)

    questions = " ".join(f"What is the access code for {n}?" for n in needles)
    (HERE / "p2_prompt.txt").write_text(
        f"The attached file is one long record dump. {questions} "
        "Answer with the three codes in the order asked, then their sum, each on its own line as `NAME = CODE` "
        "and finally `SUM = <total>`. No other text."
    )
    (HERE / "p2_expected.json").write_text(
        __import__("json").dumps({"needles": needles, "sum": sum(needles.values())})
    )
    print(f"  p2_records.txt  {len(body):>9,} chars  (~{len(body)//4:,} tokens)")
    return 0


def p3_chart() -> int:
    """A labelled bar chart, so a vision answer is either right or wrong."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names, values = ["A", "B", "C", "D", "E"], [12, 47, 83, 29, 61]
    fig, ax = plt.subplots(figsize=(6, 4), dpi=110)
    ax.bar(names, values, color="#2b6cb0")
    for n, v in zip(names, values):
        ax.text(n, v + 1.5, str(v), ha="center", fontsize=11)
    ax.set_title("POC chart: value by bar")
    ax.set_ylabel("value")
    fig.tight_layout()
    fig.savefig(HERE / "p3_chart.png")
    plt.close(fig)
    (HERE / "p3_prompt.txt").write_text(
        "Look at the attached chart image. Answer exactly two lines: `C = <value of bar C>` and "
        "`HIGHEST = <letter of the tallest bar>`. No other text."
    )
    (HERE / "p3_expected.json").write_text(__import__("json").dumps({"C": 83, "HIGHEST": "C"}))
    print("  p3_chart.png")
    return 0


def p4_video() -> int:
    """Three frames counting 1-2-3, as a video. Native video input is the unusual capability here."""
    from PIL import Image, ImageDraw

    frames = []
    for i, (n, colour) in enumerate([(1, (200, 60, 60)), (2, (60, 160, 90)), (3, (60, 90, 200))], start=1):
        im = Image.new("RGB", (480, 320), colour)
        d = ImageDraw.Draw(im)
        big = str(n * 7)
        try:
            d.text((190, 120), big, fill="white", font_size=140)
        except TypeError:                      # older Pillow: font_size unsupported
            d.text((190, 120), big, fill="white")
        p = HERE / f"p4_frame{i}.png"
        im.save(p)
        frames.append(p)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(HERE / "p4_frame%d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "1", str(HERE / "p4_numbers.mp4")],
        check=True,
    )
    (HERE / "p4_prompt.txt").write_text(
        "Look at the attached video. It shows three numbers, one per second, in order. "
        "Answer with exactly: `NUMBERS = <first>, <second>, <third>`. No other text."
    )
    (HERE / "p4_expected.json").write_text(__import__("json").dumps({"NUMBERS": [7, 14, 21]}))
    print("  p4_numbers.mp4")
    return 0


def p5_agentic() -> int:
    """A small repo with a failing test, so the fix is the check.

    This is the POC that matters for routing: opencode is an agent, so the question is whether it edits and
    re-runs rather than only describing.
    """
    d = HERE / "p5_repo"
    d.mkdir(exist_ok=True)
    (d / "calc.py").write_text(
        "def total(prices):\n"
        "    \"\"\"Sum of prices in cents.\"\"\"\n"
        "    out = 0\n"
        "    for p in prices:\n"
        "        out += p\n"
        "    return out - 1          # BUG: off by one\n"
    )
    (d / "test_calc.py").write_text(
        "from calc import total\n\n\n"
        "def test_empty():\n    assert total([]) == 0\n\n\n"
        "def test_one():\n    assert total([5]) == 5\n\n\n"
        "def test_many():\n    assert total([5, 7, 11]) == 23\n"
    )
    (HERE / "p5_prompt.txt").write_text(
        "The pytest suite in this directory fails. Find the cause and fix it so the tests pass. "
        "Run the tests to prove it. Reply with only `FIXED` once they pass."
    )
    print("  p5_repo/")
    return 0


if __name__ == "__main__":
    for fn in (p2_long_context, p3_chart, p4_video, p5_agentic):
        print(f"{fn.__name__}:")
        fn()
    print("inputs ready")
    sys.exit(0)
