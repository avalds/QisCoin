import random, os, sys
import qiskit as qk
def generate_coin_circuit(difficulty):
	circuit = qk.QuantumCircuit(1,1)
	if(difficulty == "EASY"):
		no_components = 3;
		components = [circuit.x, circuit.reset, circuit.iden]
	elif(difficulty == "MEDIUM"):
		no_components = 6;
		components = [circuit.h, circuit.x, circuit.reset, circuit.t, circuit.tdg,circuit.iden]
	elif(difficulty == "HARD"):
		no_components = 10;
		components = [circuit.h, circuit.x, circuit.reset, circuit.t, circuit.tdg,circuit.iden, circuit.h, circuit.y, circuit.z, circuit.s, circuit.sdg]
	else:
		print("ERROR")
		print(difficulty)
		print(no_components)
		sys.exit()





	for i in range(no_components):
		random.choice(components)(0)

	circuit.measure(0,0)
	return circuit

def evaluate_coin(circuit, heads):
	simulator = qk.Aer.get_backend("qasm_simulator")
	results = qk.execute(circuit, backend = simulator, shots = 1).result()
	counts = results.get_counts()
	if(counts.get(str(heads*1), 0)):
		print("congrats :)")
		return 1

	print("too bad :(")
	return 0

def setup_game():
	playing = True
	while(playing):
		games = input("Do you want to play 5, 10 or 20 games? ")
		if(games.replace(" ", "") == "1"):
			games = 1
			playing = False
		elif(games.replace(" ", "") == "5"):
			games = 5
			playing = False
		elif(games.replace(" ", "") == "10"):
			games = 10
			playing = False
		elif(games.replace(" ", "") == "20"):
			games = 20
			playing = False
		else:
			print("Unrecognized please try again!")

	playing = True
	while(playing):
		difficulty = input("Do you want easy(e), medium(m) or hard(h) difficulty? ")
		if(difficulty.replace(" ", "").upper() == "e".upper() or difficulty.replace(" ", "").upper() == "easy".upper() or difficulty.replace(" ", "") == "1"):
			difficulty = "EASY";
			playing = False;
		elif(difficulty.replace(" ", "").upper() == "m".upper() or difficulty.replace(" ", "").upper() == "medium".upper() or difficulty.replace(" ", "") == "2"):
			difficulty = "MEDIUM";
			playing = False;
		elif(difficulty.replace(" ", "").upper() == "h".upper() or difficulty.replace(" ", "").upper() == "hard".upper() or difficulty.replace(" ", "") == "3"):
			difficulty = "HARD";
			playing = False;
		else:
			print("Unrecognized please try again!")
	return games, difficulty

def play(visualization_mode = None):
	score = 0
	rounds = 0
	games, difficulty = setup_game()

	for i in range(games):
		print("The circuit is!")
		circuit = generate_coin_circuit(difficulty)
		#%matplotlib inline
		#circuit.draw(output="mpl")
		playing = True
		while(playing):
			if(visualization_mode == "mpl"): display(circuit.draw(output = "mpl"))
			else: print(circuit);
			print("heads(h)(1) or tails(t)(0)")
			choice = input()
			if(choice == "h" or choice == "heads" or choice == "" or choice == "1"):
				playing = False
				score += evaluate_coin(circuit, True)
				rounds += 1
			elif(choice == "t" or choice == "tails" or choice == "0"):
				playing = False
				score += evaluate_coin(circuit, False)
				rounds += 1
			elif(choice.upper() == "Q" or choice.upper() == "quit".upper()):
				playing = False
				print("quit!")
				return;
			else:
			    print("please enter valic input")
			if(rounds != 0):
				print("You have won {} of the {} rounds you have played ({}% winrate)".format(score, rounds, 100*score/rounds))

	if(is_highscore(games, difficulty, score/rounds)):
		name = input("It was a highscore enter your name: ")
		enter_higscore(games, difficulty, score/rounds, name)
	else:
		print("Its not a highscore!")
	print("highscores:")
	show_highscores(games, difficulty)

def is_highscore(number_of_rounds, gamemode, score, highscore_size = 3):
	folder = "HIGHSCORES/" + str(gamemode) + "/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	if(not os.path.exists(folder)):
		os.makedirs(folder)
	if(not os.path.exists(filename)):
		with open(filename, "w") as fp:
			fp.write("Baldric;0");
		return True;

	scores = []
	with open(filename, "r") as fp:
		lines = fp.readlines()

	for line in lines:
		if(len(line.split(";")) >= 2):
			scores.append(float(line.split(";")[1]))

	if(len(scores)<highscore_size):
		return True

	if(score > scores[highscore_size-1]):
		return True

	"""
	if(score == scores[highscore_size-1]):
		if(times[-1] < finish_time):
			return True
	"""
	return False

def enter_higscore(number_of_rounds, gamemode, score, name, highscore_size = 3):
	folder = "HIGHSCORES/" + str(gamemode) + "/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	with open(filename, "r") as fp:
		lines = fp.readlines()

	scores = []
	names = []
	entered = False
	for line in lines:
		if(len(line.split(";")) >= 2):
			hname, hscore = line.split(";")
			if(float(hscore) < score and not entered):
				scores.append(str(score))
				names.append(str(name))
				entered = True

			scores.append(str(hscore))
			names.append(str(hname))

	if(not entered):
		scores.append(str(score))
		names.append(str(name))
		entered = True

	#scores = scores[:highscore_size]
	#names = names[:highscore_size]
	#print(scores)
	#print(names)

	with open(filename, "w") as fp:
		for i in range(min(highscore_size,len(names))):
			fp.write(names[i])
			fp.write(";")
			fp.write(scores[i])
			fp.write("\n")

def show_highscores(number_of_rounds, gamemode):
	folder = "HIGHSCORES/" + str(gamemode) + "/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	with open(filename, "r") as fp:
		lines = fp.readlines()
	print("{:>20}|{:<20}".format("Name", "Score (%)"))
	for line in lines:
		if(len(line.split(";")) >= 2):
			hname, hscore = line.split(";")
			print("{:>20}|{:<20}".format(hname, float(hscore)*100))
