runestone build && touch build/thinkcspy/.nojekyll && \
echo 'coding101.devetry.com' > build/thinkcspy/CNAME && \
for ff in $(find build/thinkcspy/ -name '*.html'); do
    mkdir -p $(sed s/\.html$//g <<< $ff)
    cp $ff $(sed s/\.html$//g <<< $ff)/index.html
done && \
python post_process.py
