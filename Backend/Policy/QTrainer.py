import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()


    def train_step(self, state, action, reward, next_state, done):
        #Convert to tensors taht can be used for pyTorch, but not boolean Since I just use that as a normal boolean
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        
        if(len(state.shape) == 1):
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            done = (done,)

        currentModelPrediction = self.model(state) #The literal values the model generated with current weights

        target = currentModelPrediction.clone().detach()


        #Backpropagation, basically checking how good the options are in the new_state and adjust the model based on that
        for index in range(len(done)):
            correctedQValue = reward[index]
            #Of course you can't predict how good future options will be when the game already ended
            if not done[index]:
                correctedQValue = reward[index] + self.gamma * torch.max(self.model(next_state[index]))
            target[index][int(action[index])] = correctedQValue

        loss = self.criterion(currentModelPrediction, target)

        self.optimizer.zero_grad();
        loss.backward()
        self.optimizer.step()


            

        

