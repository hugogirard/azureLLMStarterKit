import { Component, EventEmitter, Input, input, Output, SimpleChanges } from '@angular/core';
import { StateService } from '../../services/state.service'
import { ChatService } from '../../services/chat.service';
import { Session } from '../../models/session';
import { NgFor, NgIf, NgClass } from '@angular/common'

@Component({
  selector: 'nav-menu',
  standalone: true,
  imports: [NgFor, NgIf, NgClass],
  templateUrl: './nav-menu.component.html',
  styleUrl: './nav-menu.component.css'
})
export class NavMenuComponent {

  @Input() newTitle: string = '';

  sessions: Session[] = [];

  selectedSession?: Session;

  @Output() sessionSelected = new EventEmitter<Session>();

  constructor(private stateService: StateService,
    private chatService: ChatService
  ) { }

  ngOnInit() {
    this.getSessionsUser();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['newTitle']) {
      if (changes['newTitle'].currentValue != null && changes['newTitle'].currentValue != '') {
        if (this.selectedSession)
          this.selectedSession.title = changes['newTitle'].currentValue;
      }
    }
  }

  selectSession(session: Session) {

    if (this.selectedSession?.sessionId == session.sessionId)
      return;

    this.selectedSession = session
    this.sessionSelected.emit(session);
  }

  createNewChat() {
    this.stateService.isLoading = true;
    this.chatService.newSession().subscribe(session => {
      this.stateService.isLoading = false;
      this.selectedSession = session ?? undefined;
      if (session) {
        session.isNewChat = true;
        this.selectedSession = session;
        this.sessionSelected.emit(session);
        this.sessions.push(session);
      }
    });
  }

  getSessionsUser() {
    this.stateService.isLoading = true;
    this.chatService.getSessions().subscribe(sessions => {
      this.stateService.isLoading = false;
      this.sessions = sessions;
      if (this.sessions.length > 0) {
        const session = sessions[0]
        this.sessionSelected.emit(session);
        this.selectedSession = session;
      }
    });
  }

  deleteSession(id: string) {

    // Replace with a better windows
    // for now we use the native browser
    const msg = 'Are you sure you want to delete this session';
    if (confirm(msg) === true) {
      this.stateService.isLoading = true;
      this.chatService.deleteSession(id)
        .subscribe(success => {
          this.stateService.isLoading = false;
          if (success) {
            this.sessions = this.sessions.filter(session => session.sessionId !== id);
            this.selectedSession = undefined;
            this.sessionSelected.emit(undefined);
          }
        })
    }
  }
}
