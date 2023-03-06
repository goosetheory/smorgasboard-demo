import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

import { BlogService } from '../../services/blog.service';
import { BlogPost } from '../../dtos/BlogPost';

@Component({
	selector: 'app-posts',
	templateUrl: './posts.component.html',
	styleUrls: ['./posts.component.scss']
})
export class PostsComponent implements OnInit {
	posts: Array<BlogPost>;

	constructor(private blogService: BlogService,
	            private titleService: Title) {
	}

	ngOnInit() {
		this.titleService.setTitle('Blog | SmorgasBoard');

		this.blogService.getAllPosts()
		.then(response => {
			this.posts = response;
		});
	}
}
