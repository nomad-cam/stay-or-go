#! /bin/bash
IMG_PATH=/home/rohshamboyha/stay-or-go/stayorgo/static/img/auto

convert state_region_overlay.png -stroke black -fill "#7ac241" -draw "rectangle 0,0 37,28" -draw "rectangle 400,100 420,120" -draw "text 425,113 'Low-Moderate'" -fill "#00adee" -draw "rectangle 37,0 78,28" -draw "rectangle 400,130 420,150" -draw "text 423,143 'High'" -fill "#fef200" -draw "rectangle 78,0 158,28" -draw "rectangle 400,160 420,180" -draw "text 425,173 'Very High'" -fill "#fe9929" -draw "rectangle 158,0 236,28" -draw "rectangle 520,100 540,120" -draw "text 545,113 'Severe'" -fill "#ef2c21" -draw "rectangle 236,0 313,28" -draw "rectangle 520,130 540,150" -draw "text 545,143 'Extreme'" -fill grey40 -draw "rectangle 313,0 624,28" -draw "rectangle 520,160 540,180" -draw "text 545,173 'Code Red'" -draw "line 63,28 63,23" -draw "line 125,28 125,23" -draw "line 188,28 188,23" -draw "line 250,28 250,23" -draw "line 375,28 375,23" -draw "line 438,28 438,23" -draw "line 500,28 500,23" -draw "line 563,28 563,23" -draw "text 200,70 '++ Note: Adapted from IDV65406 to highlight max Fire Danger Rating ++'" state_legend_overlay.png
