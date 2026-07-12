import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import copy

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.target_model = copy.deepcopy(model)
        self.target_model.eval()
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.SmoothL1Loss() #Instead of squaring loss, it checks if its large and just applies linearly if so

        self.update_counter = 0
        self.target_update_frequency = 1000

    def update_target_network(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def train_step(self, state, action, reward, next_state, done):
        #Convert to tensors taht can be used for pyTorch, but not done Since I just use that as a normal boolean
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
                with torch.no_grad():

                    #Get newer models best action
                    best_action_idx = torch.argmax(self.model(next_state[index])) 

                    #Use older models weights to update, breaks feedback loop
                    correctedQValue = reward[index] + self.gamma * self.target_model(next_state[index])[best_action_idx] 

            target[index][int(action[index])] = correctedQValue

        loss = self.criterion(currentModelPrediction, target)

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=10)
        self.optimizer.step()

        self.update_counter += 1
        if self.update_counter % self.target_update_frequency == 0:
            self.update_target_network()


            

        

