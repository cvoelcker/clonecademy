import {Component, OnInit} from '@angular/core';
import {ServerService} from '../../service/server.service'
import {ActivatedRoute, Params, Router} from '@angular/router'
import {LoaderComponent} from '../../loader/loader.component';
import {QuizEndPopupComponent} from './quiz-end-popup/quiz-end-popup.component'
import {MdDialog} from '@angular/material';

@Component({
  selector: 'app-quiz-question',
  templateUrl: './quiz-question.component.html',
  styleUrls: ['./quiz-question.component.scss']
})
/**
 * @author Leonhard Wiedmann, Claas Voelcker
 *
 * A component that implements a quiz view
 */
export class QuizQuestionComponent implements OnInit {

  courseID = -1;
  quiz = -1;
  data: any;
  id = 0;
  answers = [];
  quizSize = 0;
  done = false;
  private showFeedback: boolean;
  private loading: boolean;
  private correct: boolean;

  constructor(
    private router: Router,
    public server: ServerService,
    private route: ActivatedRoute,
    private dialog: MdDialog,
  ) {
    this.load();
    this.loading = false;
    this.correct = true;
  }

  /**
   loads data from server for current quiz id (from url)
   @author Leonhard Wiedmann
   **/
  load() {
    this.route.params.subscribe((data: Params) => {
      this.showFeedback = false;
      this.courseID = Number(data.id);
      this.server.get('courses/' + this.courseID + '/quiz/')
        .then((value: Array<any>) => {
          const array = [];
          while (value.length > 0) {
            const i = Math.floor(Math.random() * value.length);
            const item = Object.assign({}, value[i]);
            const ansArray = [];
            const answers = Object.assign([], item['answers']);
            while (answers.length > 0) {
              const j = Math.floor(Math.random() * answers.length);
              const singleItem = Object.assign({}, answers[j]);
              singleItem.chosen = false;
              ansArray.push(singleItem);
              answers.splice(j, 1)
            }
            item['answers'] = ansArray;
            array.push(item);
            value.splice(i, 1);
          }
          this.data = array;
          this.quizSize = this.data.length;
          this.id = 0
        })
    })
  }

  ngOnInit() {
  }

  /**
   sends data to server for current this.data['answers'].chosen if it is true
   @author Leonhard Wiedmann
   **/
  submit() {
    // course finished
    if (!this.showFeedback) {
      const value = [];
      const item = this.data[this.id];
      for (let i = 0; i < item['answers'].length; i++) {
        if (item['answers'][i].chosen !== undefined) {
          value.push({chosen: item['answers'][i].chosen, id: item['answers'][i].id})
        } else {
          value.push({chosen: false, id: item['answers'][i].id})
        }
      }
      this.answers.push({answers: value, id: this.data[this.id].id});

      if (this.quizSize - 1 === this.id) {
        this.done = true;
        const loader = this.dialog.open(LoaderComponent, {
          disableClose: true
        })
        this.server.post('courses/' + this.courseID + '/quiz/', {'type': 'check_answers', 'answers': this.answers}, true)
          .then(data => {
            loader.afterClosed().subscribe(stuff => {
              this.dialog.open(QuizEndPopupComponent, {data: data})
            })
            loader.close()
            // TODO show popup for end course
            // data is {name: "question of the quiz", solved: boolean "if the question is correct solved"}

          });
        return;
      } else {
        const question = this.data[this.id];

        this.showFeedback = true;
        this.loading = true;
        this.server.post('courses/' + this.courseID + '/quiz/', {'type': 'get_answers', 'id': question.id})
          .then(data => {
            this.correct = true;
            // iterates over all answers of the question and checks whether it was only selected if it is true
            // sets the attribute to true iff all correct answers and no others are selected
            for (let i = 0; i < item.answers.length; i++) {
              if (data['answers'].indexOf(item.answers[i].id) > -1) {
                question.answers[i].correct = true;
              } else {
                question.answers[i].correct = false;
              }
              if (question.answers[i].correct && (question.answers[i].chosen === false)) {
                this.correct = false
              }
            }
            this.loading = false;
          });
        return;
      }
    } else {
      this.id += 1;
      this.showFeedback = false;
    }
  }

}
