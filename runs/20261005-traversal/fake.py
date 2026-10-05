import sys, pathlib
mode, node, attempt, out = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4])
head = (f"---\nnode: {node}\nattempt: {attempt}\nengine: script\nmodel: fake\nstatus: ok\n"
        f"started: t\nended: t\nevidence: r\n---\n")
out.write_text(head + ("did the work\n" if mode == "ok" else "attempt\n"))
