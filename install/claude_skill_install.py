import os, sys, subprocess, shlex

files = os.listdir('.')
files = [f for f in files if ((not f.startswith('.')) and f.endswith('.md') and f not in ['CLAUDE.md', 'README.md'])]
files.sort()
print(f'需要安装 {len(files)} 个 skill')

if (len(sys.argv) >= 2 and sys.argv[1] in ['-c', 'clean']):
    result = input(f'请确认是否需要删除已安装的所有 skill [N/Y]: ')
    assert (result == 'Y'), "指定了 -c/clean, 未同意删除已有 skill, 无法继续"
    subprocess.check_output('rm -rf ~/.claude/skills', shell=True, stderr=sys.stderr)

os.makedirs(os.path.expanduser('~/.claude/skills'), exist_ok=True)
for f in files:
    skill_name = f[:-3]
    subprocess.check_output(f'rm -rf ~/.claude/skills/{shlex.quote(skill_name)} && mkdir -p ~/.claude/skills/{shlex.quote(skill_name)} && ln -s {shlex.quote(os.getcwd())}/{shlex.quote(f)} ~/.claude/skills/{shlex.quote(skill_name)}/SKILL.md', shell=True, stderr=sys.stderr)
subprocess.check_output(f'rm -f ~/.claude/CLAUDE.md && ln -s {shlex.quote(os.getcwd())}/CLAUDE.md ~/.claude/CLAUDE.md', shell=True, stderr=sys.stderr)

print('所有 skill 安装成功')