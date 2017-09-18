import {Component, OnInit} from '@angular/core';
import {ServerService} from '../../service/server.service'
import {ActivatedRoute, Params, Router} from '@angular/router'

@Component({
  selector: 'app-quiz-question',
  templateUrl: './quiz-question.component.html',
  styleUrls: ['./quiz-question.component.scss']
})
/**
 * @author Leonhard Wiedmann
 *
 * A component that implements a quiz view
 */
export class QuizQuestionComponent implements OnInit {

  courseID: number = -1;
  quiz: number = -1;
  data: any;
  id: number = 0;
  answers = []
  quizSize = 0;

  constructor(private router: Router, public server: ServerService, private route: ActivatedRoute) {
    this.load()
  }

  /**
   loads data from server for current quiz id (from url)
   @author Leonhard Wiedmann
   **/
  load() {
    this.route.params.subscribe((data: Params) => {
      this.courseID = Number(data.id)
      this.server.get('courses/' + this.courseID + '/quiz/').then((data: Array<any>) => {
        let array = []
        while(data.length > 0){
          let i = Math.floor(Math.random() * data.length);
          let item = Object.assign({}, data[i])
          let ansArray = []
          let answers = Object.assign([], item['answers']);
          while(answers.length >0){
            let j =  Math.floor(Math.random() * answers.length);
            let singleItem = Object.assign({}, answers[j])
            ansArray.push(singleItem)
            answers.splice(j,1)
          }
          item['answers'] = ansArray
          array.push(item)
          data.splice(i, 1);
        }
        this.data = array;
        this.quizSize = this.data.length
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
    let value = []
    let item = this.data[this.id]
    for (let i = 0; i < item['answers'].length; i++) {
      if (item['answers'][i].chosen != undefined) {
        value.push({chosen: item['answers'][i].chosen, id: item['answers'][i].id})
      }
      else {
        value.push({chosen: false, id: item['answers'][i].id})
      }
    }
    this.answers.push({answers: value, id: this.data[this.id].id})

    if (this.quizSize - 1 == this.id) {
      this.server.post('courses/' + this.courseID + '/quiz/', this.answers)
        .then(data => {
          // TODO show popup for end course
          // data is {name: "question of the quiz", solved: boolean "if the question is correct solved"}
        })
      return;
    }
    else {
      this.id += 1;
    }
  }

}
