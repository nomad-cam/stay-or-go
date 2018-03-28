#! /bin/bash
IMG_PATH=/home/rohshamboyha/stay-or-go/stayorgo/static/img/auto
#wget -q http://www.bom.gov.au/fwo/IDV65406.png > $IMG_PATH/IDV65406.png
curl http://www.bom.gov.au/fwo/IDV65406.png > $IMG_PATH/IDV65406.png
convert $IMG_PATH/IDV65406.png -stroke black -draw "line 37,27 37,1" -draw "line 78,27, 78,1" -draw "line 158,27 158,1" -draw "line 236,27 236,1" -draw "line 313,27 313,1" -fuzz 13% -fill green -opaque '#41aea4' -opaque '#0d84f4' -fuzz 8.3% -fill '#00adee' -opaque '#7abe47' -opaque '#b5d529' -fuzz 10% -fill '#00adee' -opaque '#6ac461' -fuzz 10.7% -fill '#fef200' -opaque '#f7df1e' -fuzz 10% -fill '#fe9929' -opaque '#feaa1e' -fuzz 7% -opaque '#fe8921' -fuzz 12.5% -fill '#ef2c21' -opaque '#fe4e28' -fuzz 13% -fill grey40 -opaque '#f02166' -opaque '#940b93' -fill '#7ac241' -opaque green $IMG_PATH/IDV65406_tmp.png

convert	$IMG_PATH/IDV65406_tmp.png $IMG_PATH/state_legend_overlay.png -composite $IMG_PATH/IDV65406_mod.png
