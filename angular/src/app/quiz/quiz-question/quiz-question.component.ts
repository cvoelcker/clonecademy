import { Component, OnInit } from '@angular/core';
import { ServerService } from '../../service/server.service'
import { ActivatedRoute, Params, Router } from '@angular/router'

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
  load(){
    this.route.params.subscribe((data: Params) => {
      this.courseID = Number(data.id)
      this.server.get('courses/' + this.courseID + '/quiz/').then((data) => {
        this.data = data
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
  submit(){
    let value = {}
    let item = this.data[this.id]
    for(let i = 0; i < item['answers'].length; i++){
      if (item['answers'][i].chosen != undefined){
        value[item['answers'][i].id] = item['answers'][i].chosen
      }
      else {
        value[this.data[this.id]['answers'][i].id] = false
      }
    }
    this.answers.push(value)

    if(this.quizSize -1 == this.id){
      this.server.post('courses/' + this.courseID + '/quiz/', this.answers)
          .then(data => {
            // TODO show popup for end course
            // data is {name: "question of the quiz", solved: boolean "if the question is correct solved"}
          })
      return;
    }
    else{
      this.id += 1;
    }
  }

}
