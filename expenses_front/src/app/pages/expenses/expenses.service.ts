import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BACK } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ExpensesService {
  private API = API_BACK;

  constructor(private http: HttpClient) {}

  getExpensesByMonth(month: string): Observable<any> {
    return this.http.get(`http://127.0.0.1:8000/expenses/expenses/${month}`);
  }
}
