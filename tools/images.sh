#!/bin/zsh
# Converts src-photos/* into optimised WebP in site/img. Usage: zsh tools/images.sh
cd "${0:A:h}/.."
S=src-photos; O=site/img
conv(){ # src name width
  local w=$3; cwebp -quiet -q 78 -resize $w 0 -metadata none "$S/$1" -o "$O/$2.webp"; }
# hero + stores (large)
conv p19.jpg hero-cacti 1400
conv p36.jpg store-playa 1800
conv p46.jpg store-front 1800
conv p08.jpg store-sorobon 1800
conv p06.jpg salty-shirt 1000
conv p27.jpg salty-truck 1000
conv p31.jpg salty-boys 900
# products
conv p12.webp vans-slipon 900
conv p33.webp vans-knu-skool 640
conv p47.jpg vans-knu-stacked 900
conv p49.webp vans-knu-kids 640
conv p50.jpg vans-era 600
conv p28.jpg vans-socks 900
conv p40.jpg vans-checker 736
conv p38.jpg vans-knu-close 1000
# jewelry
for f n in p07.jpg jw-charms p15.jpg jw-necklace p22.jpg jw-handchain p24.jpg jw-cuban p30.jpg jw-beads-star p32.jpg jw-bracelets p51.jpg jw-earring; do conv $f $n 1000; done
# lookbook
i=0; for f in p01.jpg p02.jpg p03.jpg p04.jpg p05.jpg p09.jpg p10.jpg p11.jpg p13.jpg p14.jpg p16.jpg p17.jpg p18.jpg p23.webp p25.jpg p26.webp p29.jpg p34.jpg p35.jpg p37.jpg p39.jpg p41.jpg p42.jpg p43.jpg p44.jpg p45.jpg p48.jpg p52.jpg p53.jpg p54.webp; do i=$((i+1)); conv $f "lb-$(printf %02d $i)" 1100; done
