import { Component } from '@angular/core';
import { NgIf } from '@angular/common'
import { StateService } from '../../services/state.service';

@Component({
  selector: 'loading',
  standalone: true,
  imports: [NgIf],
  templateUrl: './loading.component.html',
  styleUrl: './loading.component.css'
})
export class LoadingComponent {
  constructor(public stateService: StateService) { }
}
