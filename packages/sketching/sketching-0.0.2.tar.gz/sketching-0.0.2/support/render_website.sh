rm -r website_build/community
rm -r website_build/css
rm -r website_build/examples
rm -r website_build/guides
rm -r website_build/img
rm -r website_build/js

mkdir website_build/community
mkdir website_build/guides

python3 support/render_website.py ./website_src/pages.json ./website_src ./website_build

cp -r website_src/css website_build/css
cp -r website_src/img website_build/img
cp -r website_src/js website_build/js

cp -r examples website_build/examples