import random, os, sys, time
import qiskit as qk
import gym

from stable_baselines import PPO2, A2C, ACER


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

	list_components = []

	for i in range(no_components):
		index = random.choice(range(6))
		components[index](0)
		list_components.append(index)

	circuit.measure(0,0)
	return circuit, list_components

def AI_guess(AIagent,obs):
	return AIagent.predict(obs)

def measure_coin(circuit):
	simulator = qk.Aer.get_backend("qasm_simulator")
	results = qk.execute(circuit, backend = simulator, shots = 1).result()
	counts = results.get_counts()
	return int(list(counts.keys())[0])


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
		AIagent = input("Do you want to play against PPO2(p)(1), A2C(a)(2) or ACER(c)(3) agent?")
		if(AIagent.replace(" ", "").upper() == "p".upper() or AIagent.replace(" ", "").upper() == "ppo2".upper() or AIagent.replace(" ", "") == "1"):
			AIagent = PPO2.load("models/PPO2-qiscoin-v1-10k");
			ai_name = "PPO2"
			playing = False;
		elif(AIagent.replace(" ", "").upper() == "a".upper() or AIagent.replace(" ", "").upper() == "a2c".upper() or AIagent.replace(" ", "") == "2"):
			AIagent = A2C.load("models/A2C-qiscoin-v1-10k");
			ai_name = "A2C"
			playing = False;
		elif(AIagent.replace(" ", "").upper() == "c".upper() or AIagent.replace(" ", "").upper() == "acer".upper() or AIagent.replace(" ", "") == "3"):
			AIagent = ACER.load("models/ACER-qiscoin-v1-10k");
			ai_name = "ACER"
			playing = False;
		else:
			print("Unrecognized please try again!")
	return games, AIagent, ai_name

def play(visualization_mode = None):
	score = 0
	ai_score = 0
	rounds = 0
	games, agent, ai_name = setup_game()
	difficulty = "MEDIUM"
	print("You will probably not beat the AI in time, but try to beat it in accuracy :)")
	cum_time = 0 #cumulative time for player
	ai_time = 0 #cumulative time for ai


	for i in range(games):
		input("Press enter when you are ready:>>>")
		print("The circuit is!")
		circuit, list_components = generate_coin_circuit(difficulty)
		#%matplotlib inline
		#circuit.draw(output="mpl")
		playing = True
		while(playing):
			if(visualization_mode == "mpl"): display(circuit.draw(output = "mpl"))
			else: print(circuit);
			start = time.time()
			print("heads(h)(1) or tails(t)(0)")
			choice = input()
			print("\n\n")
			if(choice == "h" or choice == "heads" or choice == "" or choice == "1"):
				cum_time += time.time() - start
				start = time.time()
				AIguess = AI_guess(agent, list_components)
				ai_time += time.time() - start
				coin_value = measure_coin(circuit)
				ai_score += AIguess[0] == coin_value
				score += coin_value

				print("AI guess: {0}".format(AIguess[0]))
				playing = False

				rounds += 1
			elif(choice == "t" or choice == "tails" or choice == "0"):
				cum_time += time.time() - start
				start = time.time()
				AIguess = AI_guess(agent, list_components)
				ai_time += time.time() - start
				print("AI guess: {0}".format(AIguess[0]))
				playing = False
				coin_value = measure_coin(circuit)
				ai_score += AIguess[0] == coin_value
				score += (coin_value == 0)
				rounds += 1
			elif(choice.upper() == "Q" or choice.upper() == "quit".upper()):
				playing = False
				print("quit!")
				return;
			else:
			    print("please enter valic input")
		if(rounds != 0):
			#print("You have won {} of the {} rounds you have played ({}% winrate)".format(score, rounds, 100*score/rounds))
			#print("The AI has won {} of the {} rounds you have played ({}% winrate)".format(ai_score, rounds, 100*ai_score/rounds))
			print("\n{:^8}:{:>5}-{:<5}\n{:^8}:{:>5}-{:<5}\n{:^8}:{:>5.2f}-{:<5.2g}".format("Players","You", ai_name,"Score", score, ai_score, "Time", cum_time, ai_time))

	#print("Your time is:", time_score)
	cum_time = round(cum_time,2)
	ai_time = round_to_n(ai_time, 3)
	if(ai_score < score or (ai_score == score and ai_time > cum_time)):
		print("YOU BEAT THE AI!!!!!!")
	elif(ai_score == score and ai_time == cum_time):
		print("WOW, this should be impossible, you preformed exactly as well as the AI")
	else:
		print("You lost to the AI :( \ntry again soon!!! :)")
	time.sleep(.5)
	player_highscore = False
	ai_highscore = False
	if(is_highscore(games, difficulty, score/rounds, time_score = cum_time)):
		name = input("It was a highscore enter your name: ")
		player_highscore = True
		enter_higscore(games, difficulty, score/rounds, name, time_score = cum_time)
	else:
		print("You did not get a highscore!")
	if(is_highscore(games, difficulty, ai_score/rounds, time_score = ai_time)):
		ai_highscore = True
		enter_higscore(games, difficulty, ai_score/rounds, ai_name + "(AI)", time_score = ai_time)


	print("highscores:")
	show_highscores(games, difficulty)
	input("Well played :)")

def is_highscore(number_of_rounds, gamemode, score, highscore_size = 10, time_score = 0):
	folder = "T_HIGHSCORES_/" + str(gamemode) + "AI/"
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
	folder = "T_HIGHSCORES_/" + str(gamemode) + "AI/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	with open(filename, "r") as fp:
		lines = fp.readlines()

	scores = []
	names = []
	times = []
	entered = False
	for line in lines:
		if(len(line.split(";")) >= 3):
			hname, hscore, htime_score = line.split(";")
			if(not entered):
				if(float(hscore) < score or (float(hscore) == score and float(htime_score) > time_score)):
					scores.append(str(score).replace("\n", ""))
					names.append(str(name).replace("\n", ""))
					times.append(str(time_score).replace("\n", ""))
					entered = True

			scores.append(str(hscore).replace("\n", ""))
			names.append(str(hname).replace("\n", ""))
			times.append(str(htime_score).replace("\n", ""))

	if(not entered):
		scores.append(str(score).replace("\n", ""))
		names.append(str(name).replace("\n", ""))
		times.append(str(time_score).replace("\n", ""))
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
	folder = "T_HIGHSCORES_/" + str(gamemode) + "AI/"
	filename = folder + str(number_of_rounds)+ "highscores.csv"
	with open(filename, "r") as fp:
		lines = fp.readlines()
	print("{:^3}|{:^20}|{:^20}|{:^20}".format("No.","Name", "Score (%)", "Time (sec)"))
	placement = 1
	for line in lines:
		if(len(line.split(";")) >= 3):
			hname, hscore, htime_score = line.replace("\n", "").split(";")
			print("{0:-^3}|{0:-^20}|{0:-^20}|{0:-^20}".format("-"))
			print("{0:^3}|{1:^20}|{2:^20}|{3:^20}".format(placement, hname, float(hscore)*100, htime_score))
			placement += 1
def round_to_n(x, n = 3):
	from math import floor, log10
	return round(x, -int(floor(log10(abs(x)))) + n -1)
