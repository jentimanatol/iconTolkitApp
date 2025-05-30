git --version
git add .
git commit -m " updted interface used CSS stiles "
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.9
git push origin v1.9
pause
