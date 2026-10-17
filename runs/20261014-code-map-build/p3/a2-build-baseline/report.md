# Code-map evaluation

P2 Codex evaluator; authored independently of the future tool builder

MET records the fixture/case checks assigned to this evaluator, not a proof for all repositories. Canned-stub results test the evaluator, not a real code-map tool.

R1 marker checks run only on the bundled fixtures; held-out and external copies have no runtime marker check.

| Requirement | Status | Unchecked part |
|---|---|---|
| R1 | MET |  |
| R2 | MET |  |
| R3 | MET (tool part) | Network isolation and filesystem snapshots do not establish absence of caught connection attempts, writes outside the observed trees, putting content in git, transmission by other processes, or training use. |
| A1 | MET |  |
| A2 | NOT MET | P6 checks the agent's selection and naming of candidates it did not build. |
| A3 | MET (tool part) | P6 checks whether the agent asks the user before requesting a per-function file report. |
| A5 | MET (tool part) | P6 checks whether the agent requests a whole map without being asked. |
| A6 | NOT CHECKED |  |
| L1 | MET |  |
| L2 | NOT CHECKED |  |

## Fails-if lines

- **R1 MET** — mapping a fixture whose top level writes a marker creates that marker. Cases: R1-map, R1-chain, R1-tests, R1-callers, R1-where, R1-find, R1-callees, R1-tests-file, R1-top-level-throws.
- **R2 MET** — an implementation the lookup finds has no link. Cases: R2-all-implementations, R2-type-not-name-source.
- **R2 MET** — a declaration is presented as proof of an implementation. Cases: R2-declaration.
- **R2 MET** — a test fake is unlabelled or presented as the real implementation. Cases: R2-test-fake.
- **R2 MET** — an unresolved or ambiguous target is unmarked. Cases: R2-ambiguous, R2-unresolved, R2-type-not-name-test, R2-no-tests-pattern.
- **R3 MET (tool part)** — protected content leaves the machine or enters git. Cases: R3-offline.
  - Unchecked: Network isolation and filesystem snapshots do not establish absence of caught connection attempts, writes outside the observed trees, putting content in git, transmission by other processes, or training use.
- **A1 MET** — a claim lacks its location or contradicts the code, or a checked example misses a known item. Cases: A1-module-siblings, A1-no-sibling-rule, A1-map-link-flow, A1-known-callers, A1-known-callees, A1-shared-and-varies, A1-const-map.
- **A2 MET (tool part)** — a known place is not found. Cases: A2-find-known, A2-const-find-comment, A2-const-find-string.
  - Unchecked: P6 checks the agent's selection and naming of candidates it did not build.
- **A2 MET (tool part)** — an ambiguous match is treated as certain, or a candidate not built is not named. Cases: A2-ambiguous-find, A2-ambiguous-callers, A2-effect-step-ambiguous.
  - Unchecked: P6 checks the agent's selection and naming of candidates it did not build.
- **A2 NOT MET** — a known link within the depth is missing, or a shown link contradicts the code. Cases: A2-known-chain, A2-default-six-down, A2-default-six-up, A2-explicit-depth, A2-computed-member, A2-const-chain, A2-const-chain-through, A2-const-callers, A2-const-callees, A2-inline-generator-owner, A2-same-name-helper-fake, A2-shorter-route-down, A2-shorter-route-down-reversed, A2-shorter-route-up, A2-shorter-route-up-reversed.
  - Unchecked: P6 checks the agent's selection and naming of candidates it did not build.
- **A2 MET (tool part)** — a link lacks its kind or location. Cases: A2-link-kind-location.
  - Unchecked: P6 checks the agent's selection and naming of candidates it did not build.
- **A2 MET (tool part)** — a function reached twice is shown twice. Cases: A2-shared-once, A2-recursion.
  - Unchecked: P6 checks the agent's selection and naming of candidates it did not build.
- **A3 MET (tool part)** — the count differs from the list, or a link lacks its evidence. Cases: A3-count-evidence, A3-same-name-helper-not-counted.
  - Unchecked: P6 checks whether the agent asks the user before requesting a per-function file report.
- **A3 MET (tool part)** — a test with a known path is missing. Cases: A3-known-path, A3-fake-unset, A3-fake-count, A3-fake-exclude, A3-user-pattern-outside-test-folder, A3-const-tests.
  - Unchecked: P6 checks whether the agent asks the user before requesting a per-function file report.
- **A3 MET (tool part)** — static links are called coverage. Cases: A3-static-label.
  - Unchecked: P6 checks whether the agent asks the user before requesting a per-function file report.
- **A3 MET (tool part)** — the per-function file report runs without the user's request. Cases: A3-no-file-report.
  - Unchecked: P6 checks whether the agent asks the user before requesting a per-function file report.
- **A5 MET (tool part)** — an answer comes only inside a dump or without its evidence or limits, or a whole map is produced unasked. Cases: A5-specific-answer, A5-default-text, A5-exact-callees, A5-exact-not-found, A5-exact-depth-stop.
  - Unchecked: P6 checks whether the agent requests a whole map without being asked.
- **A6 NOT CHECKED** — fewer than three modules are mapped, or a map fails A1. Cases: none.
  - No opencode case files for the three modules were supplied.
- **L1 MET** — a branch stops early without a reason, or an empty result is presented as proof of absence. Cases: L1-empty, L1-dynamic, L1-outside-repository, L1-depth-zero, L1-computed-member, L1-no-blanket-limit.
- **L2 NOT CHECKED** — it leaves out correctness, the build cost, the reading tokens or the time, or hides a worse result. Cases: none.
  - P5 measures cost against reading; this evaluator does not measure L2.

## Failures

### A2-shorter-route-down (A2)

Case file: /home/smoke01/dev/ancient-games/code_map/eval/cases/fixtures.json

Arguments: `["chain","route-depth/down.ts:1","--up","0","--down","3","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/services/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/ambiguity/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/unresolved/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/chain/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/map/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/marker/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/typed-twins/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/computed/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/named-tests/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/classified/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/const-held/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/answer-scope/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/effect-inline/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/effect-shadow/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/effect-twins/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/route-depth/tsconfig.json","--root","/home/smoke01/dev/ancient-games/code_map/eval/fixtures","--tests","**/*.testcase.ts","--json"]`

Exit: 0. Isolation: true.

```json
[
  {
    "path": "chain.down[].children[].link.to",
    "expected": {
      "includes": {
        "file": "route-depth/down.ts",
        "line": 8
      }
    },
    "actual": [
      {
        "file": "route-depth/down.ts",
        "line": 6,
        "endLine": 6,
        "name": "routeShared",
        "kind": "function",
        "testFake": false
      },
      {
        "file": "route-depth/down.ts",
        "line": 7,
        "endLine": 7,
        "name": "routeLeaf",
        "kind": "function",
        "testFake": false
      }
    ],
    "message": "includes location check failed"
  },
  {
    "path": "chain.down[].children[].children[].link",
    "expected": [
      {
        "from": {
          "file": "route-depth/down.ts",
          "line": 7,
          "name": "routeLeaf",
          "kind": "function"
        },
        "site": {
          "file": "route-depth/down.ts",
          "line": 7
        },
        "kind": "call",
        "resolution": "implementation",
        "to": {
          "file": "route-depth/down.ts",
          "line": 8,
          "name": "routeTail",
          "kind": "function"
        },
        "candidates": [
          {
            "file": "route-depth/down.ts",
            "line": 8,
            "name": "routeTail",
            "kind": "function",
            "testFake": false
          }
        ],
        "via": "definition"
      }
    ],
    "actual": [
      {
        "from": {
          "file": "route-depth/down.ts",
          "line": 6,
          "endLine": 6,
          "name": "routeShared",
          "kind": "function"
        },
        "site": {
          "file": "route-depth/down.ts",
          "line": 6,
          "endLine": 6
        },
        "kind": "call",
        "resolution": "implementation",
        "candidates": [
          {
            "file": "route-depth/down.ts",
            "line": 7,
            "endLine": 7,
            "name": "routeLeaf",
            "kind": "function",
            "testFake": false
          }
        ],
        "via": "definition",
        "declaration": {
          "file": "route-depth/down.ts",
          "line": 7,
          "endLine": 7
        },
        "to": {
          "file": "route-depth/down.ts",
          "line": 7,
          "endLine": 7,
          "name": "routeLeaf",
          "kind": "function",
          "testFake": false
        }
      }
    ],
    "message": "shape check failed"
  }
]
```

Tool stdout:
```text
{"command":"chain","query":["route-depth/down.ts:1"],"limits":[{"at":{"file":"route-depth/down.ts","line":1},"reason":"depth","text":"chain depth 0 up and 3 down"}],"chain":{"up":[],"down":[{"level":1,"link":{"from":{"file":"route-depth/down.ts","line":1,"endLine":4,"name":"routeRoot","kind":"function"},"site":{"file":"route-depth/down.ts","line":2,"endLine":2},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/down.ts","line":5,"endLine":5,"name":"routeA","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/down.ts","line":5,"endLine":5},"to":{"file":"route-depth/down.ts","line":5,"endLine":5,"name":"routeA","kind":"function","testFake":false}},"children":[{"level":2,"link":{"from":{"file":"route-depth/down.ts","line":5,"endLine":5,"name":"routeA","kind":"function"},"site":{"file":"route-depth/down.ts","line":5,"endLine":5},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/down.ts","line":6,"endLine":6,"name":"routeShared","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/down.ts","line":6,"endLine":6},"to":{"file":"route-depth/down.ts","line":6,"endLine":6,"name":"routeShared","kind":"function","testFake":false}},"children":[{"level":3,"link":{"from":{"file":"route-depth/down.ts","line":6,"endLine":6,"name":"routeShared","kind":"function"},"site":{"file":"route-depth/down.ts","line":6,"endLine":6},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/down.ts","line":7,"endLine":7,"name":"routeLeaf","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/down.ts","line":7,"endLine":7},"to":{"file":"route-depth/down.ts","line":7,"endLine":7,"name":"routeLeaf","kind":"function","testFake":false}},"children":[],"stop":{"reason":"depth"}}]}]},{"level":1,"link":{"from":{"file":"route-depth/down.ts","line":1,"endLine":4,"name":"routeRoot","kind":"function"},"site":{"file":"route-depth/down.ts","line":3,"endLine":3},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/down.ts","line":6,"endLine":6,"name":"routeShared","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/down.ts","line":6,"endLine":6},"to":{"file":"route-depth/down.ts","line":6,"endLine":6,"name":"routeShared","kind":"function","testFake":false}},"children":[],"stop":{"reason":"seen","ref":{"file":"route-depth/down.ts","line":6}}}]}}

```
Tool stderr:
```text

```

### A2-shorter-route-up (A2)

Case file: /home/smoke01/dev/ancient-games/code_map/eval/cases/fixtures.json

Arguments: `["chain","route-depth/up.ts:1","--up","3","--down","0","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/services/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/ambiguity/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/unresolved/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/chain/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/map/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/marker/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/typed-twins/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/computed/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/named-tests/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/classified/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/const-held/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/answer-scope/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/effect-inline/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/effect-shadow/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/effect-twins/tsconfig.json","--project","/home/smoke01/dev/ancient-games/code_map/eval/fixtures/route-depth/tsconfig.json","--root","/home/smoke01/dev/ancient-games/code_map/eval/fixtures","--tests","**/*.testcase.ts","--json"]`

Exit: 0. Isolation: true.

```json
[
  {
    "path": "chain.up[].children[].link.from",
    "expected": {
      "includes": {
        "file": "route-depth/up.ts",
        "line": 5
      }
    },
    "actual": [
      {
        "file": "route-depth/up.ts",
        "line": 3,
        "endLine": 3,
        "name": "routeShared",
        "kind": "function"
      },
      {
        "file": "route-depth/up.ts",
        "line": 4,
        "endLine": 4,
        "name": "routeLeaf",
        "kind": "function"
      }
    ],
    "message": "includes location check failed"
  },
  {
    "path": "chain.up[].children[].children[].link",
    "expected": [
      {
        "from": {
          "file": "route-depth/up.ts",
          "line": 5,
          "name": "routeTail",
          "kind": "function"
        },
        "site": {
          "file": "route-depth/up.ts",
          "line": 5
        },
        "kind": "call",
        "resolution": "implementation",
        "to": {
          "file": "route-depth/up.ts",
          "line": 4,
          "name": "routeLeaf",
          "kind": "function"
        },
        "candidates": [
          {
            "file": "route-depth/up.ts",
            "line": 4,
            "name": "routeLeaf",
            "kind": "function",
            "testFake": false
          }
        ],
        "via": "definition"
      }
    ],
    "actual": [
      {
        "from": {
          "file": "route-depth/up.ts",
          "line": 4,
          "endLine": 4,
          "name": "routeLeaf",
          "kind": "function"
        },
        "site": {
          "file": "route-depth/up.ts",
          "line": 4,
          "endLine": 4
        },
        "kind": "call",
        "resolution": "implementation",
        "candidates": [
          {
            "file": "route-depth/up.ts",
            "line": 3,
            "endLine": 3,
            "name": "routeShared",
            "kind": "function",
            "testFake": false
          }
        ],
        "via": "definition",
        "declaration": {
          "file": "route-depth/up.ts",
          "line": 3,
          "endLine": 3
        },
        "to": {
          "file": "route-depth/up.ts",
          "line": 3,
          "endLine": 3,
          "name": "routeShared",
          "kind": "function",
          "testFake": false
        }
      }
    ],
    "message": "shape check failed"
  }
]
```

Tool stdout:
```text
{"command":"chain","query":["route-depth/up.ts:1"],"limits":[{"at":{"file":"route-depth/up.ts","line":1},"reason":"depth","text":"chain depth 3 up and 0 down"}],"chain":{"up":[{"level":1,"link":{"from":{"file":"route-depth/up.ts","line":2,"endLine":2,"name":"routeA","kind":"function"},"site":{"file":"route-depth/up.ts","line":2,"endLine":2},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/up.ts","line":1,"endLine":1,"name":"routeRoot","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/up.ts","line":1,"endLine":1},"to":{"file":"route-depth/up.ts","line":1,"endLine":1,"name":"routeRoot","kind":"function","testFake":false}},"children":[{"level":2,"link":{"from":{"file":"route-depth/up.ts","line":3,"endLine":3,"name":"routeShared","kind":"function"},"site":{"file":"route-depth/up.ts","line":3,"endLine":3},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/up.ts","line":2,"endLine":2,"name":"routeA","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/up.ts","line":2,"endLine":2},"to":{"file":"route-depth/up.ts","line":2,"endLine":2,"name":"routeA","kind":"function","testFake":false}},"children":[{"level":3,"link":{"from":{"file":"route-depth/up.ts","line":4,"endLine":4,"name":"routeLeaf","kind":"function"},"site":{"file":"route-depth/up.ts","line":4,"endLine":4},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/up.ts","line":3,"endLine":3,"name":"routeShared","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/up.ts","line":3,"endLine":3},"to":{"file":"route-depth/up.ts","line":3,"endLine":3,"name":"routeShared","kind":"function","testFake":false}},"children":[],"stop":{"reason":"depth"}}]}]},{"level":1,"link":{"from":{"file":"route-depth/up.ts","line":3,"endLine":3,"name":"routeShared","kind":"function"},"site":{"file":"route-depth/up.ts","line":3,"endLine":3},"kind":"call","resolution":"implementation","candidates":[{"file":"route-depth/up.ts","line":1,"endLine":1,"name":"routeRoot","kind":"function","testFake":false}],"via":"definition","declaration":{"file":"route-depth/up.ts","line":1,"endLine":1},"to":{"file":"route-depth/up.ts","line":1,"endLine":1,"name":"routeRoot","kind":"function","testFake":false}},"children":[],"stop":{"reason":"seen","ref":{"file":"route-depth/up.ts","line":3}}}],"down":[]}}

```
Tool stderr:
```text

```

## Parts not checked

- **A2 NOT CHECKED** — P6 checks the agent's selection and naming of candidates it did not build.
- **A3 NOT CHECKED** — P6 checks whether the agent asks the user before requesting a per-function file report.
- **A5 NOT CHECKED** — P6 checks whether the agent requests a whole map without being asked.
- **R3 NOT CHECKED** — Network isolation and filesystem snapshots do not establish absence of caught connection attempts, writes outside the observed trees, putting content in git, transmission by other processes, or training use.

## Totals

```json
{
  "requirements": {
    "MET": 7,
    "NOT MET": 1,
    "NOT CHECKED": 2
  },
  "lines": {
    "MET": 17,
    "NOT MET": 1,
    "NOT CHECKED": 2
  },
  "cases": {
    "MET": 68,
    "NOT MET": 2,
    "NOT CHECKED": 0
  }
}
```
