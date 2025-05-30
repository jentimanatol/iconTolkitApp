git --version
git add .
git commit -m " default filename will be something like app_icon_16×16.ico "
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v1.8
git push origin v1.8
pause
