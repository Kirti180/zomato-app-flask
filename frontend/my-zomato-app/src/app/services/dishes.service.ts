import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DishesService {
  private baseUrl = 'https://zomato-dugp.onrender.com/dishes'; // Replace with your backend API URL

  constructor(private http: HttpClient) {}

  getDishes(): Observable<any[]> {
    return this.http.get<any[]>(this.baseUrl);
  }

  createDish(dish: any): Observable<any> {
    return this.http.post<any>(this.baseUrl, dish);
  }

  updateDish(dish: any): Observable<any> {
    const url = `${this.baseUrl}/${dish.id}`;
    return this.http.put<any>(url, dish);
  }

  deleteDish(dishId: number): Observable<any> {
    const url = `${this.baseUrl}/${dishId}`;
    return this.http.delete<any>(url);
  }
}
