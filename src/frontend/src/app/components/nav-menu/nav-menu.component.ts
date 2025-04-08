import { Component } from '@angular/core';
import { StateService } from '../../services/state.service'
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'nav-menu',
  standalone: true,
  imports: [],
  templateUrl: './nav-menu.component.html',
  styleUrl: './nav-menu.component.css'
})
export class NavMenuComponent {

  constructor(private stateService: StateService,
    private chatService: ChatService
  ) { }

  createNewChat() {
    this.stateService.isLoading = true;
    this.chatService.newSession().subscribe(session => {
      this.stateService.isLoading = false;
      console.log(session);
    });
  }
}
