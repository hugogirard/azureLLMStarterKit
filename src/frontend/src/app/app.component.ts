import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavMenuComponent } from './components/nav-menu/nav-menu.component';
import { ChatpaneComponent } from './components/chatpane/chatpane.component';
import { LoadingComponent } from './components/loading/loading.component';
import { HttpClientModule } from '@angular/common/http';
import { Session } from './models/session';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,
    NavMenuComponent,
    ChatpaneComponent,
    LoadingComponent,
    HttpClientModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  selectedSession?: Session

  onNewSelectedSession(newSelectedSession: Session) {
    this.selectedSession = newSelectedSession
  }
}
