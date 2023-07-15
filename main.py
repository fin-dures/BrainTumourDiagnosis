from neural_net import *
from file_handler import *
from gui import *
from testing import *
from time import sleep

X_RES = 50
Y_RES = 50




def create_expected_matrix(negatives, positives):

    
    pos = [1]*positives
    neg = [0]*negatives
    
    matrix=[]
    matrix.append(pos)
    matrix.append(neg)
    
    return matrix





def process_event(event, values, root, image_data, network):

    

    window_mapper = {
"Enter images for training": root.add_training_buttons, "Enter images for testing": root.add_testing_buttons,
"Enter images for diagnosis": root.add_diagnosis_buttons, "Back": root.add_home_buttons

              }


    
    if event in window_mapper:
        window_mapper[event]()
        root.update()
        return image_data, network
        
    else:
        match event:
            
            case "Select positive images for training":
                try:
                    image_data["training_positives"] = get_image_matrix(X_RES, Y_RES)
                except:
                    root.add_error_message("error")
                    root.update()

                    sleep(2)
                    print('slept')
                    root.clear()
                    root.add_home_buttons()
                    root.update()
                    return image_data, network
                    

            case "Select negative images for training":
                image_data["training_negatives"] = get_image_matrix(X_RES, Y_RES)

            case "Select positive images for testing":
                image_data["testing_positives"] = get_image_matrix(X_RES, Y_RES)

            case "Select negative images for testing":
                image_data["testing_negatives"] = get_image_matrix(X_RES, Y_RES)

            case "Select image for diagnosis":
                image_data["diagnosis_image"] = get_single_image(X_RES, Y_RES)

            case "Train":
                if len(image_data["training_positives"])<=1 or len(image_data["training_negatives"])<=1:
                    return image_data, network
                
                network, image_data["average_value"] = train_network(network, image_data["training_positives"], image_data["training_negatives"])
                save_matrix(network.weights0, "weights0.txt")
                save_matrix(network.weights1, "weights1.txt")
                save_value(image_data["average_value"], "average.txt")
                

            case "Diagnose":
                if image_data["diagnosis_image"]==None or image_data["average_value"]==None or len(image_data["diagnosis_image"])<1:
                    return image_data, network

                result = diagnose(network, image_data["average_value"], image_data["diagnosis_image"])
                if result:
                    result = "Positive"
                else:
                    result = "Negative"

                root.add_diagnosis_buttons(result)
                root.update()

            case "Test":
                if len(image_data["testing_positives"])<1 or len(image_data["testing_negatives"])<1 or len(image_data["average_value"])<1:
                    return image_data, network

                result = test(network, image_data["average_value"], image_data["testing_positives"], image_data["testing_negatives"], values[0])
                root.add_testing_buttons(result)
                root.update()
                
                
            case other:
                raise Exception("Event has no asocciated action")

    return image_data, network

def main():

    loaded = False
    try:
        weights0, weights1 = load_matrix("weights0.txt"), load_matrix("weights1.txt")
        average = load_value("average.txt")
        loaded = True
    except FileNotFoundError:
        average=None
    
    
    if loaded:
        network = neural_network(X_RES*Y_RES, 2, weights0=weights0, weights1=weights1)
    else:
        network = neural_network(X_RES*Y_RES, 2)


    root = main_window("Brain tumour diagnoser")
    root.add_home_buttons()
    root.open()
    image_data = {"training_positives":[], "training_negatives":[], "diagnosis_image":[], "testing_positives":[], "testing_negatives":[], "average_value": average}
    while True:
        event, values = root.loop()

        if event == sg.WIN_CLOSED:
            exit()


        if event!=None:
            image_data, network = process_event(event, values, root, image_data, network)
            




def train_network(network, positives, negatives):
    
    TRAINING_SESSIONS = 10
    LEARNING_RATE = -0.1
    UPDATE_FREQUENCY = 5
    
    
    expected_matrix = create_expected_matrix(len(negatives), len(positives))

    positives+=(negatives)
    

    
    average=network.train_network(positives, expected_matrix, LEARNING_RATE, TRAINING_SESSIONS, UPDATE_FREQUENCY)


    return network, average


#True = positive, False = negative
def diagnose(network, average, vector):
    while True:

        result = network.feed_forward(vector)
        if result[0]>average:
            return True
        else:
            return False
            
        
def test(network, average, positives, negatives, significance):
    
    trials = len(positives)+len(negatives)
    successes=0
    positives_correct=0
    negatives_correct=0
    test1 = binomial_test(network, significance, trials, 0.5)
    
    for image in positives:
        if diagnose(network, average, image):
            successes+=1
            positives_correct+=1
    

    for image in negatives:
        if not diagnose(network, average, image):
            successes+=1
            negatives_correct+=1



    estimated_accuracy = successes/trials
    estimated_sensitivity = positives_correct/len(positives)
    estimated_specificity = negatives_correct/len(negatives)
    
    success, probability = test1.test(successes)
    
    if success:
        result = "succesful: indicating that the program is working correctly"
        short_result="Succesful"
    else:
        result= "unsuccesful: indicating the the program is not working correctly or has not been properly trained"
        short_result="Unsuccesful"
        
    message = """The program diagnosed {successes} images correctly out of {total} total images.
The probability of this happening by chance is {prob}% hence the test is {result}.
Estimated accuracy = {eac}%
Estimated sensitivity = {ese}%
Estimated specificity = {esp}%
""".format(successes=successes, total=trials, result=result, prob=round(probability*100, 1), eac= round(estimated_accuracy*100,1), ese = round(estimated_sensitivity*100,1), esp=round(estimated_specificity*100,1))
    
    print(message)

    
    short_message = "Result: {res}% \nEstimated accuracy: {ea}% \nEstimated specificity: {esp}% \nEstimated sensitivity: {ese}%".format(ea=round(estimated_accuracy*100,1), esp=round(estimated_specificity*100,1), ese=round(estimated_sensitivity*100,1), res=short_result)
    return short_message


    
    
    
    

if __name__ == "__main__":
    main()
