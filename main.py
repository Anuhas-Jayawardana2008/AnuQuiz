from tkinter import simpledialog,messagebox,filedialog
import pygame
import sys

pygame.init()

FONT = pygame.font.Font("components\impact.ttf", 40)
STAGE = "menu"

pygame.display.set_caption("AnuQuiz Program")

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

#button info (menu)
create_quiz_button_img = pygame.image.load("components/create.png")
create_quiz_button_rect = create_quiz_button_img.get_rect(topleft=(0,100))
answer_quiz_button_img = pygame.image.load("components/answer.png")
answer_quiz_button_rect = answer_quiz_button_img.get_rect(topleft=(0,300))
quit_button_img = pygame.image.load("components/quit.png")
quit_button_rect = quit_button_img.get_rect(topleft=(0,500))

#button info (creator)
back_menu_button_img = pygame.image.load("components/back_menu.png")
back_menu_button_rect = back_menu_button_img.get_rect(topright=(800,0))
edit_question_button_img = pygame.image.load("components\edit.png")
edit_answer_button_img = pygame.image.load("components\edit.png")

next_button_img = pygame.image.load("components/next.png")
next_button_rect = next_button_img.get_rect(bottomright=(800,600)) 

save_button_img = pygame.image.load("components\save.png")
save_button_rect = save_button_img.get_rect(topright=(800,100))

back_button_img = pygame.image.load("components/back.png")
back_button_rect = back_button_img.get_rect(bottomleft=(0,600)) 

edit_question_button_rect = edit_question_button_img.get_rect(topleft=(400,300))
edit_answer_button_rect = edit_answer_button_img.get_rect(topleft=(400,360))

delete_question_button_img = pygame.image.load("components\delete.png")
delete_question_button_rect = delete_question_button_img.get_rect(center=(400,300),midbottom=(400,600))

creator_questions = ["Your question here"]
creator_answers = ["Your answer here"]
creator_questions_current = 0

# info (client)

client_questions = []
client_answers = []
client_questions_current = 0
client_loaded = False
client_temp = []

edit_answer_img = pygame.image.load("components\edit.png")
edit_answer_rect = edit_answer_img.get_rect(topleft=(400,360))

back_img = pygame.image.load("components/back.png")
back_rect = back_img.get_rect(bottomleft=(0,600)) 

next_img = pygame.image.load("components/next.png")
next_rect = next_img.get_rect(bottomright=(800,600)) 

submit_img = pygame.image.load("components\submit.png")
submit_rect = submit_img.get_rect(topright=(800,0))

bk = pygame.image.load("components/back.png")
bk_rect = bk.get_rect(bottomleft=(0,600))

while True:
    screen.fill("light blue")
    clock.tick(120)

    click = False
    mouse_point = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    if STAGE == "submit":
        done = False
        score = 0
        if not done:
            score = 0
            for i in range(len(client_answers)):
                if client_answers[i] == client_temp[i]:
                    score += 10
            done = True

        if bk_rect.collidepoint(mouse_point) and click:
            STAGE = "menu"
        screen.blit(FONT.render("Results", True, 'black'),(0,0))
        screen.blit(FONT.render(f"Score : {score} out of {len(client_answers) * 10}", True, 'black'),(0,300))
        screen.blit(bk,bk_rect)

    if STAGE == "client":
        valid = False
        path = None
        if not client_loaded:
            path = filedialog.askopenfilename(title="Open Save file")
            if path:
                with open(path,'r') as file:
                    content = file.read()
                    if content.startswith("###"):
                        client_loaded = True
                        _mixed = content.splitlines()
                        _stop_index = _mixed.index("???")
                        _temp_questions = []
                        _temp_answers = []
                        for i in range(1,_stop_index):
                            _temp_questions.append(_mixed[i][::-1])
                        for i in range(_stop_index + 1,len(_mixed)):
                            _temp_answers.append(_mixed[i][::-1])
                        client_questions = _temp_questions
                        client_answers = _temp_answers
                        for i in range(len(client_questions)):
                            client_temp.append("Your Answer here...")
                    else:
                        messagebox.showerror("Error","Invalid save file")
                        STAGE = "menu"

        try:
            screen.blit(FONT.render("AnuQuiz - Answer Quiz", True, 'black'),(0,0))
            screen.blit(FONT.render(f"Question {client_questions_current + 1} of {len(client_questions)}", True, 'black'),(0,60))
            screen.blit(FONT.render(f"{client_questions[client_questions_current]}",True,'black'),(0,300))
            screen.blit(FONT.render(f"{client_temp[client_questions_current]}", True, 'black'),(0,360))

            if client_questions_current == len(client_questions) - 1:
                screen.blit(submit_img,submit_rect)
                if submit_rect.collidepoint(mouse_point) and click:
                    STAGE = "submit"

            if edit_answer_rect.collidepoint(mouse_point) and click:
                _new_ans = simpledialog.askstring("New Answer", "Enter your new answer ")
                if _new_ans:
                    client_temp[client_questions_current] = _new_ans

            if next_rect.collidepoint(mouse_point) and click:
                if client_questions_current + 1 < len(client_questions): 
                    client_questions_current += 1
                else:
                    creator_questions_current += 1

            if back_rect.collidepoint(mouse_point) and click:
                if client_questions_current == 0:
                    if messagebox.askokcancel("Warning!","You will be sent back to the menu") == True:
                        STAGE = "menu"
                else:
                    client_questions_current -= 1
        except:
            STAGE = "menu"

        screen.blit(back_img,back_rect)
        screen.blit(next_img,next_rect)
        screen.blit(edit_answer_img,edit_answer_rect)

    if STAGE == "menu":
        client_temp = []
        client_loaded = False
        creator_questions = ["Your question here"]
        creator_answers = ["Your answer here"]
        creator_questions_current = 0

        client_questions = []
        client_answers = []
        client_questions_current = 0

        if quit_button_rect.collidepoint(mouse_point) and click:
            pygame.quit()
            sys.exit()
        if create_quiz_button_rect.collidepoint(mouse_point) and click:
            STAGE = "creator"
        if answer_quiz_button_rect.collidepoint(mouse_point) and click:
            STAGE = "client"
        screen.blit(create_quiz_button_img, create_quiz_button_rect)
        screen.blit(answer_quiz_button_img, answer_quiz_button_rect)
        screen.blit(quit_button_img, quit_button_rect)
        screen.blit(FONT.render("AnuQuiz - A Quiz Editor",True,'black'),(0,0))

    if STAGE == "creator":
        screen.blit(FONT.render("AnuQuiz - Create Quiz", True, 'black'),(0,0))
        screen.blit(FONT.render(f"Question {creator_questions_current + 1} of {len(creator_questions)}", True, 'black'),(0,60))

        screen.blit(edit_question_button_img,edit_question_button_rect)
        screen.blit(edit_answer_button_img,edit_answer_button_rect)

        screen.blit(next_button_img,next_button_rect)
        screen.blit(back_button_img,back_button_rect)
        screen.blit(delete_question_button_img,delete_question_button_rect)
        screen.blit(save_button_img,save_button_rect)

        if save_button_rect.collidepoint(mouse_point) and click:
            path = filedialog.asksaveasfilename(title="Save Quiz")
            if path:
                with open(path,'w') as file:
                    file.write("###\n")
                with open(path,'a') as file:
                    for i in range(len(creator_questions)):
                        file.write(creator_questions[i][::-1] + "\n")
                    file.write("???\n")
                    for i in range(len(creator_answers)):
                        file.write(creator_answers[i][::-1] + "\n")
                    messagebox.showinfo("Done","Your quiz was save successfully!");

        if delete_question_button_rect.collidepoint(mouse_point) and click:
            if len(creator_questions) == 1:
                messagebox.showerror("Error","This is the last question, press back to go to the main menu")
            else:
                creator_questions.remove(creator_questions[creator_questions_current])
                creator_answers.remove(creator_answers[creator_questions_current])
                creator_questions_current = len(creator_questions) - 1

        if back_button_rect.collidepoint(mouse_point) and click:
            if creator_questions_current == 0:
                if messagebox.askokcancel("Warning!","You will be sent back to the menu") == True:
                    STAGE = "menu"
            else:
                creator_questions_current -= 1

        if next_button_rect.collidepoint(mouse_point) and click:
            # if the question exists
            if creator_questions_current + 1 < len(creator_questions): 
                creator_questions_current += 1
            else:
                # create new question
                creator_questions.append("Your question here")
                creator_answers.append("Your answer here")
                creator_questions_current += 1

        if edit_question_button_rect.collidepoint(mouse_point) and click:
            _new_question = simpledialog.askstring("Edit", "Enter the new question")
            if _new_question:
                creator_questions[creator_questions_current] = _new_question

        if edit_answer_button_rect.collidepoint(mouse_point) and click:
            _new_answer = simpledialog.askstring("Edit","Enter new answer")
            if _new_answer:
                creator_answers[creator_questions_current] = _new_answer

        screen.blit(FONT.render(f"{creator_questions[creator_questions_current]}",True,'black'),(0,300))
        screen.blit(FONT.render(f"{creator_answers[creator_questions_current]}", True, 'black'),(0,360))
        
        screen.blit(back_menu_button_img,back_menu_button_rect)
        if back_menu_button_rect.collidepoint(mouse_point) and click:
            STAGE = "menu"
            
    pygame.display.update()

pygame.quit()
sys.exit()