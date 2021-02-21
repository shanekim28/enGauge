import { Component, NgModule } from '@angular/core';
//import { BrowserModule } from '@angular/platform-browser';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import {DataService} from "./app.service";
declare var require: any;
const localData: any = require('./data2.json');
const chartNum = 5;
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers:[DataService]
})
export class AppComponent {
  chartData: any[] = [];
  processedRowData:any[] = [];


  columns = [{ name:'Rank',  prop: 'rank'},{ name:'First Name',  prop: 'firstName' }, { name:'Last Name',  prop: 'lastName' }, { name: 'Points', prop:'points' }];
  rows: any[];

  view: any[] = [700, 400];

  // options
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Student';
  showYAxisLabel = true;
  yAxisLabel = 'Points';

  colorScheme = {
    domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
  };

  constructor(private dataService: DataService) {
    this.setUpDataFromServer();
    //this.setUpLocalData();
  }

  private setUpDataFromServer() {
    this.dataService.getServerData().subscribe(response => {
      const serverData:any = response;
      for (let i = 0; i < chartNum; i++) {
        let currentStudent: any = serverData[i];
        let temp = [];
        this.chartData.push({
          name: currentStudent.firstname + " " + currentStudent.lastname,
          value: currentStudent.points
        });
        this.chartData = [...this.chartData];
      }
      serverData.forEach(user => {
        this.processedRowData.push({
          rank: this.processedRowData.length + 1,
          firstName: user.firstname,
          lastName: user.lastname,
          points: user.points
        });
      });
      this.rows = [...this.processedRowData];
    });
  }

  private setUpLocalData() {
      for (let i = 0; i < chartNum; i++) {
        let currentStudent: any = localData[i];
        let temp = [];
        this.chartData.push({
          name: currentStudent.firstname + " " + currentStudent.lastname,
          value: currentStudent.points
        });
        this.chartData = [...this.chartData];
      }
      localData.forEach(user => {
        this.processedRowData.push({
          rank: this.processedRowData.length + 1,
          firstName: user.firstname,
          lastName: user.lastname,
          points: user.points,
        });
      });
      this.rows = [...this.processedRowData];
  }


  onSelect(event) {
    console.log(event);
  }

  updateFilter(event) {
    const val:string = event.target.value.toLowerCase();
    const words:string[] = val.split(" ");
    this.rows = [...this.processedRowData];
    if (words.length===0) {
      return;
    }
    const temp:any[] = this.processedRowData.filter(row => {
        let match:boolean = true;
        words.forEach(word=>{
          if (row.firstName.toLowerCase().indexOf(word)<0 && row.lastName.toLowerCase().indexOf(word)<0) {
            match = false;
          }
        });
        return match;
    });
    this.rows = [...temp];
  }
}
