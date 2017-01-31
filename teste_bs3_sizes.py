IMG_RATIO = 9.0/16 # 16:9, 8:5 etc.
BSLIMIT = 1200.0 # (bs_container_width_max/ncols*ncols_miolo)-(gutter*2)
G = 10

for x in xrange(1,13):
    print x, (BSLIMIT/x)-(G*2)

print IMG_RATIO, BSLIMIT

# http://codepen.io/alexeiramone/pen/mRXwpz