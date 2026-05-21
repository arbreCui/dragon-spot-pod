#!/usr/bin/env python3
"""Minimal make_depend.py for the Dragon build system.

Two modes invoked from the per-library Makefiles:

  make_depend.py [files/globs ...]
      Print a topologically sorted list of source files (one line, space
      separated). Used to populate SRC90 so consumers compile after their
      module producers under sequential `make`. Parallel `make` relies on
      the .deps.mk file (mode 2) for ordering.

  make_depend.py --make-deps [files/globs ...]
      Emit Make rules of the form `consumer.o: producer.o ...` for every
      `use FOO` -> `module FOO` edge. Files with no inter-module deps
      produce no output.

Handles both free-form (.f90/.F90) and fixed-form (.f/.F/.for) Fortran.
Skips intrinsic modules (iso_c_binding, iso_fortran_env, ieee_*, omp_lib,
mpi*). Treats `module procedure` (interface body) as not a module decl.
"""
import sys
import os
import re
import glob

INTRINSIC = {
    'iso_c_binding', 'iso_fortran_env',
    'ieee_arithmetic', 'ieee_exceptions', 'ieee_features',
    'omp_lib', 'omp_lib_kinds',
    'mpi', 'mpi_f08',
}

USE_RE = re.compile(r'^\s*use\s+(?:,\s*\w+\s*::\s*)?(\w+)', re.IGNORECASE)
MODULE_RE = re.compile(r'^\s*module\s+(\w+)', re.IGNORECASE)


def is_fixed_form(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in ('.f', '.for')


def is_comment(line, fixed_form):
    s = line.lstrip()
    if not s:
        return True
    if s.startswith('!'):
        return True
    if fixed_form and line and line[0] in 'Cc*':
        return True
    return False


def parse_file(path):
    """Return (defined_modules, used_modules) as lowercase sets."""
    fixed = is_fixed_form(path)
    defined, used = set(), set()
    try:
        with open(path, 'r', errors='replace') as f:
            for raw in f:
                if is_comment(raw, fixed):
                    continue
                # Strip inline ! comment (string literals not handled; the
                # heuristic is good enough for `use`/`module` statements).
                line = raw.split('!', 1)[0]
                m = USE_RE.match(line)
                if m:
                    name = m.group(1).lower()
                    if name not in INTRINSIC:
                        used.add(name)
                    continue
                m = MODULE_RE.match(line)
                if m:
                    name = m.group(1).lower()
                    if name == 'procedure':
                        continue
                    defined.add(name)
    except OSError:
        pass
    return defined, used


def expand_args(args):
    files = []
    seen = set()
    for a in args:
        matches = sorted(glob.glob(a)) if any(c in a for c in '*?[') else (
            [a] if os.path.exists(a) else []
        )
        for m in matches:
            if m not in seen:
                seen.add(m)
                files.append(m)
    return files


def build_dep_graph(parsed):
    """parsed: {file: (defined, used)}. Returns {file: set(file dep)}."""
    mod2file = {}
    for f, (defs, _) in parsed.items():
        for m in defs:
            mod2file[m] = f
    deps = {f: set() for f in parsed}
    for f, (_, uses) in parsed.items():
        for u in uses:
            producer = mod2file.get(u)
            if producer and producer != f:
                deps[f].add(producer)
    return deps, mod2file


def topo_sort(files, deps):
    visited = {}
    order = []

    def visit(node):
        st = visited.get(node, 0)
        if st == 2:
            return
        if st == 1:
            return  # cycle: ignore (shouldn't happen for valid Fortran)
        visited[node] = 1
        for d in sorted(deps.get(node, ())):
            visit(d)
        visited[node] = 2
        order.append(node)

    for f in files:
        visit(f)
    return order


def obj_name(src):
    return os.path.splitext(os.path.basename(src))[0] + '.o'


def main():
    args = sys.argv[1:]
    make_deps = False
    if args and args[0] == '--make-deps':
        make_deps = True
        args = args[1:]
    files = expand_args(args)
    parsed = {f: parse_file(f) for f in files}
    deps, _ = build_dep_graph(parsed)
    if make_deps:
        for f in sorted(parsed):
            producers = sorted(deps.get(f, ()))
            if producers:
                print(f"{obj_name(f)}: {' '.join(obj_name(p) for p in producers)}")
    else:
        print(' '.join(topo_sort(files, deps)))


if __name__ == '__main__':
    main()
