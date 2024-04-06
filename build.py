import shutil
import subprocess
import os


def build_pmd_automation() -> None:
	subprocess.run(
		['pyinstaller', 'GUI.py', '-F', '--name', 'automation', '--noconsole']
	)
	original_file_path = 'secrets.txt'
	dist_dir = os.path.join(os.getcwd(), 'dist')
	copy_file_path = os.path.join(dist_dir, 'secrets.txt')
	shutil.copy(original_file_path, copy_file_path)


if __name__ == '__main__':
	build_pmd_automation()
