import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Session } from '../models/session'
import { Observable, of } from 'rxjs';
import { environment } from '../environments/environment';
import { catchError, tap } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class ChatService {

    constructor(
        private http: HttpClient) { }

    newSession(): Observable<Session | null> {
        return this.http.post<Session>(`${environment.apiBaseUrl}/api/session/new`, null)
            .pipe(
                tap(_ => {
                    if (!environment.production)
                        console.log('creating new session');
                }),
                catchError(this.handleError<Session>('newSession'))
            )
    }

    getSessions(): Observable<Session[]> {
        return this.http.get<Session[]>(`${environment.apiBaseUrl}/api/session/all`)
            .pipe(
                tap(x => {
                    if (!environment.production)
                        console.log(`${x.length} sessions found`);
                }),
                catchError(this.handleError<Session[]>('getSessions', [])))
    }

    /**
     * Handle Http operation that failed.
     * Let the app continue.
     *
     * @param operation - name of the operation that failed
     * @param result - optional value to return as the observable result
     */
    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {

            console.error(error);

            return of(result as T);
        };
    }
}
