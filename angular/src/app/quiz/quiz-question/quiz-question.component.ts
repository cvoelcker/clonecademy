import {Component, OnInit} from '@angular/core';
import {ServerService} from '../../service/server.service'
import {ActivatedRoute, Params, Router} from '@angular/router'

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

  courseID: number = -1;
  quiz: number = -1;
  data: any;
  id: number = 0;
  answers = [];
  quizSize = 0;
  private showFeedback: boolean;
  private real_answers: any;
  private loading: boolean;
  private correct: boolean;

  constructor(private router: Router, public server: ServerService, private route: ActivatedRoute) {
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
      this.server.get('courses/' + this.courseID + '/quiz/').then((data: Array<any>) => {
        let array = [];
        while (data.length > 0) {
          let i = Math.floor(Math.random() * data.length);
          let item = Object.assign({}, data[i]);
          let ansArray = [];
          let answers = Object.assign([], item['answers']);
          while (answers.length > 0) {
            let j = Math.floor(Math.random() * answers.length);
            let singleItem = Object.assign({}, answers[j]);
            ansArray.push(singleItem);
            answers.splice(j, 1)
          }
          item['answers'] = ansArray;
          array.push(item);
          data.splice(i, 1);
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
    if (!this.showFeedback) {
      let value = [];
      let item = this.data[this.id];
      for (let i = 0; i < item['answers'].length; i++) {
        if (item['answers'][i].chosen != undefined) {
          value.push({chosen: item['answers'][i].chosen, id: item['answers'][i].id})
        }
        else {
          value.push({chosen: false, id: item['answers'][i].id})
        }
      }
      this.answers.push({answers: value, id: this.data[this.id].id});

      if (this.quizSize - 1 == this.id) {
        this.server.post('courses/' + this.courseID + '/quiz/', {'type': 'check_answers', 'answers': this.answers})
          .then(data => {
            // TODO show popup for end course
            // data is {name: "question of the quiz", solved: boolean "if the question is correct solved"}
          });
        return;
      }
      else {
        const item = this.data[this.id];
        this.showFeedback = true;
        this.loading = true;
        this.server.post('courses/' + this.courseID + '/quiz/', {'type': 'get_answers', 'id': item.id - 1})
          .then(data => {
            this.correct = true;
            for (let i = 0; i < item.answers.length; i++) {
              if (data['answers'].indexOf(item.answers[i].id) > -1) {
                item.answers[i].correct = true;
              } else {
                item.answers[i].correct = false;
              }
              if (item.answers[i].correct != (item.answers[i].chosen != null)) {
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
