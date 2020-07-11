
import os 
import sys 
import shutil
import argparse
import itertools 
from pathlib import Path

"""
make の基準でファイルを複製するべきか判定します
"""

def should_copy (src, dist):
  if Path(dist).exists():
    disttime = Path(dist).stat().st_mtime 
    srctime = Path(src).stat().st_mtime
    return disttime < srctime
  return True

"""
ファイルを複製します
"""

def copy_file (src, dist):
  if should_copy(src, dist):
    print("%s => %s" % (src, dist)) # for logging!
    shutil.copyfile(src, dist)

"""
パターンからファイルの一覧を取得します
"""

def list_file_by_pattern (pattern, basedir):
  if "/" not in pattern:
    return Path(basedir).glob("**/" + pattern)
  else:
    return Path(basedir).glob(pattern)

"""
.gitignore 形式のファイルから複製対象と排除対象の一覧を取得します
"""

def read_ignorefile (src, *, basedir):
  excludes = set()
  includes = set()
  with open(src, "r") as stream:
    for line in stream:
      stripped = line.strip()
      if stripped.startswith("#"):
        pass
      elif stripped.startswith("!"):
        includes.update(list_file_by_pattern(stripped[1:], basedir))
      else:
        excludes.update(list_file_by_pattern(stripped, basedir))
  return includes, excludes

"""
指定されたファイルから複製対象と排除対象のファイル一覧を取得します
ファイルが存在していなかった場合この関数は空の集合を返します
"""

def try_read_ignorefile (file, *, basedir):
  ignorefile = Path(basedir).joinpath(file)
  if ignorefile.exists():
    return read_ignorefile(ignorefile, basedir=basedir)
  return set(), set()

"""
指定されたファイルの一覧から複製対象と排除対象のファイル一覧を取得します
"""

def try_read_ignorefiles (files, *, basedir):
  includes = set()
  excludes = set()
  for file in files:
    newincludes, newexcludes = try_read_ignorefile(file, basedir=basedir)
    includes.update(newincludes)
    excludes.update(newexcludes)
  return includes, excludes

"""
ディレクトリを作成します
"""

def make_dir (path):
  if not Path(path).exists():
    print("make directory => %s" % (path,)) # for logging!
    os.makedirs(path, exist_ok=True)

"""
ディレクトリを複製します
"""

def copy_dir (src, dist, *, includes, excludes, ignorefiles):
  make_dir(dist)
  newincludes, newexcludes = try_read_ignorefiles(ignorefiles, basedir=src)
  for file in os.listdir(src):
    newsrc = Path(src).joinpath(file)
    newdist = Path(dist).joinpath(file)
    copy(
      newsrc, 
      newdist, 
      includes=includes.union(newincludes), 
      excludes=excludes.union(newexcludes), 
      ignorefiles=ignorefiles
    )

"""
指定されたディレクトリあるいはファイルを複製します
"""

def copy (src, dist, *, includes=set(), excludes=set(), ignorefiles=set()):
  if (Path(src) in includes or
      Path(src) not in excludes):
    if Path(src).is_dir():
      copy_dir(src, dist, includes=includes, excludes=excludes, ignorefiles=ignorefiles)
    else:
      copy_file(src, dist)

"""
シェルから実行される際に呼出される関数です
"""

def main ():
  parser = argparse.ArgumentParser(description="copy git managed directory to other without ignored by .gitignore.")
  parser.add_argument("src", type=Path, help="source directory.")
  parser.add_argument("dist", type=Path, help="dist directory.")
  parser.add_argument("--includes", nargs="*", default=set(), help="include files.")
  parser.add_argument("--excludes", nargs="*", default=set(), help="exclude files.")
  parser.add_argument("--ignore-files", nargs="*", default=set(), help="text files that list ignore pattern like as .gitignore.")
  arguments = parser.parse_args()
  includes = map(Path, arguments.includes)
  excludes = map(Path, arguments.excludes)
  ignorefiles = itertools.chain(map(Path, arguments.ignore_files), (Path(".gitignore"),))
  copy_dir(
    arguments.src, 
    arguments.dist,
    includes = set(includes),
    excludes = set(excludes),
    ignorefiles = set(ignorefiles))

if __name__ == "__main__":
  main()
