import random, os, sys, time
import qiskit as qk
from IPython.display import clear_output

def generate_coin_circuit(difficulty):
	circuit = qk.QuantumCircuit(1,1)
	if(difficulty == "EASY"):
		no_components = 3;
		components = [circuit.x, circuit.reset, circuit.iden]
	elif(difficulty == "MEDIUM"):
		no_components = 6;
		components = [circuit.h, circuit.x, circuit.reset, circuit.t, circuit.tdg, circuit.iden]
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
	input("Are you ready?>>>")
	print("The timer starts in:\n3")
	time.sleep(1)
	print("2")
	time.sleep(1)
	print("1")
	time.sleep(1)
	print("Go")

	start = time.time()

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
			clear_output()
			print("You have won {} of the {} rounds you have played ({}% winrate)".format(score, rounds, 100*score/rounds))

	time_score = round(time.time()-start, 2)
	print("Your time is:", time_score)
	if(is_highscore(games, difficulty, score/rounds, time_score = time_score)):
		#clear_output()
		name = input("It was a highscore enter your name: ")
		name = name[:30].replace(";", "") #To ensure that the name is not overly long
		enter_higscore(games, difficulty, score/rounds, name, time_score = time_score)
	else:
		print("Its not a highscore!")
	print("highscores:")
	show_highscores(games, difficulty)

def is_highscore(number_of_rounds, gamemode, score, highscore_size = 10, time_score = 0):
	folder = "T_HIGHSCORES/" + str(gamemode) + "/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	if(not os.path.exists(folder)):
		os.makedirs(folder)
	if(not os.path.exists(filename)):
		with open(filename, "w") as fp:
			fp.write("Baldric;0;0");
		return True;

	scores = []
	times = []
	with open(filename, "r") as fp:
		lines = fp.readlines()

	for line in lines:
		line = line.replace("\n", "")
		if(len(line.split(";")) >= 3):
			scores.append(float(line.split(";")[1]))
			times.append(float(line.split(";")[2]))

	if(len(scores)<highscore_size):
		return True

	if(score > scores[highscore_size-1]):
		return True


	if(score == scores[highscore_size-1]):
		if(times[-1] > time_score):
			return True

	return False

def enter_higscore(number_of_rounds, gamemode, score, name, highscore_size = 10, time_score = 0):
	folder = "T_HIGHSCORES/" + str(gamemode) + "/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	with open(filename, "r") as fp:
		lines = fp.readlines()

	scores = []
	names = []
	times = []
	entered = False
	for line in lines:
		line = line.replace("\n", "")
		if(len(line.split(";")) >= 3):
			hname, hscore, htime_score = line.split(";")
			if(not entered):
				if(float(hscore) < score or (float(hscore) == score and float(htime_score) > time_score)):
					scores.append(str(score))
					names.append(str(name))
					times.append(str(time_score))
					entered = True

			scores.append(str(hscore))
			names.append(str(hname))
			times.append(str(htime_score))

	if(not entered):
		scores.append(str(score))
		names.append(str(name))
		times.append(str(time_score))
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
			fp.write(";")
			fp.write(times[i])
			fp.write("\n")

def show_highscores(number_of_rounds, gamemode):
	folder = "T_HIGHSCORES/" + str(gamemode) + "/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	with open(filename, "r") as fp:
		lines = fp.readlines()
	print("{:^3}|{:^30}|{:^20}|{:^20}".format("No.","Name", "Score (%)", "Time (sec)"))
	placement = 1
	for line in lines:
		if(len(line.split(";")) >= 3):
			hname, hscore, htime_score = line.replace("\n", "").split(";")
			print("{0:-^3}|{0:-^30}|{0:-^20}|{0:-^20}".format("-"))
			print("{0:^3}|{1:^30}|{2:^20}|{3:^20}".format(placement, hname, float(hscore)*100, htime_score))
			placement += 1
