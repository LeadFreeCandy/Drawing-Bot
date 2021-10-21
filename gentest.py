def spiral_out(x,y, spiral_radius):
    
    for j in range(1,spiral_radius+1):
        for i in range(x-j,x+j+1):
            yield (i,y+j)
            yield (i,y-j)
        for i in range(y-j+1, y+j):
            yield (x+j,i)
            yield (x-j,i)

gen = spiral_out(0,0,1)
print(list(gen))