import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import { Contenido } from '../models/contenido';

@Injectable({
  providedIn: 'root'
})
export class COMPILADORService {

  API_URI = 'https://peaceful-shelf-02245.herokuapp.com';

  constructor(private http: HttpClient, private router: Router) { }

  COMPILAR(Contenidos: Contenido): any{
    return this.http.post<any>(`${this.API_URI}/Compilar/`, Contenidos);
  }

  GRAFICAR(Contenidos: Contenido): any{
    return this.http.post<any>(`${this.API_URI}/GRAFICAR/`, Contenidos);
  }
}
