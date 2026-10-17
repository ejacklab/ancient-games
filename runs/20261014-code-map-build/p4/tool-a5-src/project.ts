import ts from "typescript";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";

/** An object literal written where a service type is expected, and every type it stands for. */
export interface WrittenObject {
  literal: ts.ObjectLiteralExpression;
  owners: ts.Symbol[];
}

/** What one run has already worked out, so a question about the program is answered once, not once per call site. */
export interface AnalysisCache {
  readonly implementationsByMember: Map<ts.Symbol, Map<string, ts.Declaration[]>>;
  writtenObjects?: WrittenObject[];
}

export interface Project {
  readonly root: string;
  readonly program: ts.Program;
  readonly checker: ts.TypeChecker;
  readonly files: ts.SourceFile[];
  readonly cache: AnalysisCache;
  pathOf(node: ts.Node | ts.SourceFile | string): string | undefined;
  /** True when the declaration is repository source the map may claim, not a library or ambient file. */
  isSource(node: ts.Node | undefined): boolean;
  sourceOf(loc: { file: string }): ts.SourceFile | undefined;
}

function parseProjectConfig(projectPath: string): { options: ts.CompilerOptions; fileNames: string[] } {
  const absolute = resolve(projectPath);
  const config = ts.readConfigFile(absolute, ts.sys.readFile);
  if (config.error) throw new Error(ts.flattenDiagnosticMessageText(config.error.messageText, " "));
  const parsed = ts.parseJsonConfigFileContent(config.config, ts.sys, dirname(absolute), undefined, absolute);
  if (parsed.errors.length) {
    const first = parsed.errors[0]!;
    throw new Error(ts.flattenDiagnosticMessageText(first.messageText, " "));
  }
  return { options: parsed.options, fileNames: parsed.fileNames };
}

function toRelative(root: string, fileName: string): string | undefined {
  const absolute = resolve(fileName);
  const rel = relative(root, absolute);
  if (!rel || rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) return undefined;
  return rel.split(sep).join("/");
}

export function createProject(projectPaths: string[], root: string): Project {
  if (!projectPaths.length) throw new Error("at least one --project tsconfig.json is required");
  const parsed = projectPaths.map(parseProjectConfig);
  const options: ts.CompilerOptions = { ...parsed[0]!.options, noEmit: true };
  const fileNames = new Set<string>();
  for (const project of parsed) for (const fileName of project.fileNames) fileNames.add(fileName);
  const currentDirectory = dirname(resolve(projectPaths[0]!));

  const host: ts.LanguageServiceHost = {
    getScriptFileNames: () => [...fileNames],
    getScriptVersion: () => "1",
    getScriptSnapshot: fileName => {
      const text = ts.sys.readFile(fileName);
      return text === undefined ? undefined : ts.ScriptSnapshot.fromString(text);
    },
    getCurrentDirectory: () => currentDirectory,
    getCompilationSettings: () => options,
    getDefaultLibFileName: () => ts.getDefaultLibFilePath(options),
    fileExists: fileName => ts.sys.fileExists(fileName),
    readFile: fileName => ts.sys.readFile(fileName),
    readDirectory: (path, extensions, exclude, include, depth) =>
      ts.sys.readDirectory(path, extensions, exclude, include, depth),
    directoryExists: directory => ts.sys.directoryExists(directory),
    getDirectories: directory => ts.sys.getDirectories(directory),
  };

  const program = ts.createLanguageService(host, ts.createDocumentRegistry()).getProgram();
  if (!program) throw new Error("the TypeScript program could not be built from the given projects");

  const absoluteRoot = resolve(root);
  const pathOf = (node: ts.Node | ts.SourceFile | string): string | undefined => {
    const fileName = typeof node === "string" ? node : ts.isSourceFile(node) ? node.fileName : node.getSourceFile().fileName;
    return toRelative(absoluteRoot, fileName);
  };
  const sourceOf = (loc: { file: string }): ts.SourceFile | undefined =>
    program.getSourceFile(resolve(absoluteRoot, loc.file));

  const files = program.getSourceFiles()
    .filter(file => !file.isDeclarationFile && !file.fileName.includes("/node_modules/") && pathOf(file) !== undefined)
    .sort((left, right) => (pathOf(left)! < pathOf(right)! ? -1 : pathOf(left)! > pathOf(right)! ? 1 : 0));

  const sourceFiles = new Set(files.map(file => file.fileName));
  return {
    root: absoluteRoot,
    program,
    checker: program.getTypeChecker(),
    files,
    cache: { implementationsByMember: new Map() },
    pathOf,
    isSource: node => Boolean(node && sourceFiles.has(node.getSourceFile().fileName)),
    sourceOf,
  };
}