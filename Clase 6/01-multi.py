import multiprocessing

def saludar():
    print("Hola desde nodo: ", __name__)

if __name__ == "__main__":
	p1 = multiprocessing.Process(target=saludar)
	p2 = multiprocessing.Process(target=saludar)
	p1.start()
	p2.start()
	p1.join()
	p2.join()
