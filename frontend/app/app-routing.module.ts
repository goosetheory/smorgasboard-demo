import { AddPhotoComponent } from './add-photo/add-photo.component';
import { AllPhotosComponent } from './all-photos/all-photos.component';
import { ArchiveComponent } from './archive/archive.component';
import { AuthGuard } from './auth-guard';
import { BoardComponent } from './board/board.component';
import { BoardsComponent } from './boards/boards.component';
import { CheckoutComponent } from './checkout/checkout.component';
import { ContactUsComponent } from './contact-us/contact-us.component';
import { CookiesPolicyComponent } from './cookies-policy/cookies-policy.component';
import { CreateBoardComponent } from './create-board/create-board.component';
import { FaqComponent } from './faq/faq.component';
import { FourOhFourComponent } from './four-oh-four/four-oh-four.component';
import { GetStartedComponent } from './get-started/get-started.component';
import { HomepageComponent } from './homepage/homepage.component';
import { JoinBoardComponent } from './join-board/join-board.component';
import { LoginComponent } from './login/login.component';
import { LoveToScanComponent } from './love-to-scan/love-to-scan.component';
import { NgModule } from '@angular/core';
import { PrivacyPolicyComponent } from './privacy-policy/privacy-policy.component';
import { PostsComponent } from './blog/posts/posts.component';
import { PostComponent } from './blog/post/post.component';
import { RouterModule, Routes } from '@angular/router';
import { TermsOfServiceComponent } from './terms-of-service/terms-of-service.component';

const routes: Routes = [
{ path: '', component: HomepageComponent },
{ path: 'add-photo/:boardID', component: AddPhotoComponent },
{ path: 'archive/:boardID', component: ArchiveComponent },
{ path: 'blog', component: PostsComponent },
{ path: 'blog/:slug', component: PostComponent },
{ path: 'board/:boardID', component: BoardComponent, canActivate: [AuthGuard] },
{ path: 'board/:boardID/manage-photos', component: AllPhotosComponent, canActivate: [AuthGuard] },
{ path: 'board', component: BoardComponent, canActivate: [AuthGuard] },
{ path: 'boards', component: BoardsComponent, canActivate: [AuthGuard]},
{ path: 'checkout', component: CheckoutComponent, canActivate: [AuthGuard]},
{ path: 'contact-us', component: ContactUsComponent },
{ path: 'cookies-policy', component: CookiesPolicyComponent },
{ path: 'create-board', component: CreateBoardComponent, canActivate: [AuthGuard] },
{ path: 'faq', component: FaqComponent },
{ path: 'free-trial', redirectTo: '/create-board?boardType=1' },
{ path: 'get-started', component: GetStartedComponent },
{ path: 'i-love-scanning-qr-codes', component: LoveToScanComponent },
{ path: 'join-board/:boardID', component: JoinBoardComponent, canActivate: [AuthGuard] },
{ path: 'login', component: LoginComponent },
{ path: 'privacy-policy', component: PrivacyPolicyComponent },
{ path: 'terms-of-service', component: TermsOfServiceComponent },
{ path: '404', component: FourOhFourComponent },
{ path: 'dj', redirectTo: 'photo-booth-for-djs' },
{ path: '**', redirectTo: '/404' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule],
    providers: [AuthGuard]
})

export class AppRoutingModule { }
