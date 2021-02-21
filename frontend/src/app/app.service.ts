import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable()
export class DataService {
  constructor(private http: HttpClient) { }
  getServerData() {
    return this.http.get("http://09f5a8030481.ngrok.io/api/leaderboard", {});
  }
}
