
import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


ON = 255
OFF = 0
vals = [ON, OFF]

def addGlider(i,j,grid, N):
    glider = np.array([[0, 0, 255],[255, 0, 255],[0, 255, 255]])
    if i == 1 and j == 1:
        glider = np.array([[0, 255, 0],[0, 0, 255],[255, 255, 255]])
    elif i == N-4 and j == N-4:
        glider = np.array([[255, 255, 0],[255, 0, 255],[255, 0, 0]])
    elif i == 1 and j == N-4:
        glider = np.array([[0, 255, 0],[255, 0, 0],[255, 255, 255]])
    elif i == N-4 and j == 1:
        glider = np.array([[255, 255, 255],[0, 0, 255],[0, 255, 0]])

    grid[i:i+3, j:j+3] = glider
    

def randomGrid(N):
    # print("sadasd")
    return np.random.choice(vals, N*N, p=[0.2,0.8]).reshape(N,N)

def update(freamNum, img, grid , N):

    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

            if newGrid[i,j]== ON:
                if (total<2) or (total>3):
                    newGrid[i,j]= OFF
            else:
                if total==3:
                    newGrid[i,j] = ON

    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


def main():

    parser =argparse.ArgumentParser(description = "Runs Conway's Game of Life Simulation")

    parser.add_argument('--grid-size', dest="N", required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    # parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--gliders', action='store_true', required=False)
    

    args= parser.parse_args()

    N = 100

    if args.N and int(args.N) > 8:
        N= int(args.N)

    updateInterval = 50
    # if args.interval:
    #     updateInterval = int(args.interval)

    grid= np.array([])

    if args.gliders:
        grid = np.zeros(N*N).reshape(N,N)
        for i in range(4):
            # print(N)
            if i == 0:
                addGlider(1, 1, grid, N)
                pass
            elif(i == 1):
                addGlider(1, N-4, grid, N)
                pass
            elif(i == 2):
                addGlider(N-4, 1, grid, N)
                pass
            elif(i == 3):
                addGlider(N-4, N-4, grid, N)
                pass
    else:
        grid = randomGrid(N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation = 'nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=300,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()     
    # print("hola3")
    if args.movfile:
        ani.save(args.movfile, writer='ffmpeg', fps=30)
    

if __name__ == '__main__':
    main()




