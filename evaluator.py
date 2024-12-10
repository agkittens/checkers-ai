
import torch
import torch.nn as nn
import torch.optim as optim
from checkers import *
from model import CheckersEvaluator


def penalize(states, model, gamma, optimizer):
    total_loss = 0.0
    for i in range(len(states) ):
        state = states[i]
        current_value = model(state)


        # expected_value = current_value * gamma * (1.0 + 0.2*i/len(states)) + random.Random.gauss(random.Random(),0,1.0)

        board_value = evaluate_board(state)
        if board_value >0:
            expected_value = torch.Tensor([board_value,0])
        else:
            expected_value = torch.Tensor([0,-board_value])

        # expected_value = current_value/2  # + evaluate_board(state)*(1-gamma)



        # expected_value = -1.0*i/len(states) + gamma * current_value + random.Random.gauss(random.Random(),0,1.0)

        loss = nn.MSELoss()(current_value, expected_value)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        total_loss += loss.item()
    return total_loss

def award(states, model, gamma, optimizer, factor):
    total_loss = 0.0
    for i in range(len(states) ):
        state = states[i]
        current_value = model(state)

        # expected_value = current_value / gamma * (1.0 + 0.2*i/len(states))

        if factor >0:
            expected_value = torch.Tensor([100.0 * (i / len(states)),0])
        else:
            expected_value = torch.Tensor([0,100.0 * (i / len(states))])

        # expected_value = 1.0*i/len(states) + gamma * current_value

        loss = nn.MSELoss()(current_value, expected_value)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        total_loss += loss.item()
    return total_loss


def print_board(board):
    for row in board:
        for element in row:
            if element == 0:
                print(" ", end="")
            if element == 1:
                print("w", end="")
            if element == 4:
                print("W", end="")
            if element == -1:
                print("b", end="")
            if element == -4:
                print("B", end="")
        print()
        # print()
    pass


def train_rl(model, optimizer, gamma=0.99, epochs=100):

    for epoch in range(epochs):
        total_loss = 0.0

        board = initialize_board()
        current_turn = 0
        current_player = "white"
        states = []

        while not is_game_over(board) and current_turn < 200:
            if current_player == "white":
                # print("White AI is thinking...")
                move = select_best_move_ai(board, 1, "white", model) # model should have own func
                if move:
                    board = make_move(board, move)
                current_player = "black"

            else:
                # print("Black player's turn")
                move = select_best_move(board, 1, "black")
                if move:
                    board = make_move(board, move)
                current_player = "white"
            states.append(deepcopy(board))
            current_turn +=1
        who_won = is_game_over(board)
        print_board(board)

        if who_won == 100:
            print(current_turn, "ai won")

            total_loss = award(states, model, gamma, optimizer)
        else:
            print(current_turn, ";(")
            total_loss = penalize(states, model, gamma, optimizer)




        print(f'Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(states)}')


def train_rl_duo(model1,model2, optimizer1,optimizer2, gamma=0.9, epochs=100):

    for epoch in range(epochs):
        total_loss = 0.0

        board = initialize_board()
        current_turn = 0
        current_player = "white"
        states = []

        while not is_game_over(board) and current_turn < 200:
            if current_player == "white":
                # print("White AI is thinking...")
                move = select_best_move_ai(board, 4, "white", model1) # model should have own func
                if move:
                    board = make_move(board, move)
                current_player = "black"

            else:
                # print("Black player's turn")
                move = select_best_move_ai(board, 4, "black", model2) # model should have own func

                # move = select_best_move(board, 7, "black")
                if move:
                    board = make_move(board, move)
                current_player = "white"
            states.append(deepcopy(board))
            current_turn +=1
        who_won = is_game_over(board)
        print_board(board)

        if who_won == 100:
            print(current_turn, "white won")

            total_loss = award(states, model1, gamma, optimizer1, 1)
            total_loss = penalize(states, model2, gamma, optimizer2)


        elif who_won == -100:
            print(current_turn, "black one")
            total_loss = penalize(states, model1, gamma, optimizer1)
            total_loss = award(states, model2, gamma, optimizer2, -1)

        else:
            print(current_turn)
            total_loss = penalize(states, model1, gamma, optimizer1)
            total_loss = penalize(states, model2, gamma, optimizer2)








        print(f'Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(states)}')


if __name__ == "__main__":
    model1 = CheckersEvaluator()

    model1.load_state_dict("model3.pth")
    model2 = CheckersEvaluator()

    model2.load_state_dict("model4.pth")


    optimizer1 = optim.Adam(model1.parameters(), lr=0.001)
    optimizer2 = optim.Adam(model2.parameters(), lr=0.001)



    train_rl_duo(model1,model2, optimizer1,optimizer2, epochs=100)

    torch.save(model1.state_dict(), 'model3.pth')
    torch.save(model1.state_dict(), 'model4.pth')

