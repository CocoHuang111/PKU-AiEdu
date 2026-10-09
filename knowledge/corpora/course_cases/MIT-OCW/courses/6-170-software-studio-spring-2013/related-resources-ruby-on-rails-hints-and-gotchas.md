- Source: https://ocw.mit.edu/courses/6-170-software-studio-spring-2013/pages/related-resources/ruby-on-rails-hints-and-gotchas/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Related Resources Ruby on Rails: Hints and Gotcha's

- Start the server: `rails s`
- Open a Rails console: `rails c`
- Create a controller/action/view/route all in one step: `rails generate controller controller_name action_name`
- Set up a new route (in `config/routes.rb`): `"/my/route" => "controller_name#action_name"`
- Set up a new route with a parameter (in `config/routes.rb`): `"/item/:item_id" => "controller_name#action_name"`
- Access a route parameter, GET query argument, or POST data in a controller or view: `params[:parameter_name]`
- Insert some Ruby code into a view: `3 plus 4 equals <%= 3+4 %>`
- Create a model and its migration: `rails generate model Product name:string description:text`
- Run the migrations locally (you have to do this every time you add a migration): `rake db:migrate`
- Run the migrations on Heroku (you have to do this every time you add a migration): `heroku run rake db:migrate`
- The file `db/schema.rb` tells you what the current shape of your database is. This useful to look at during development!
- Use simple, singular names for your models in camel case, like `StoreProduct`.
- Use GET for routes that should be crawl-able by a search engine.
- Use POST for routes that mutate the state of the database, or for logging in.
- For Project 1.2, you will have to deal with the same-origin policy.
- Models in Rails correspond to tables in the database.
- The model is named `LikeThis`. The corresponding table is named `like_this`.
- `This` that look like `:this` are called “symbols.” Python does not have this. You can think of them like immutable, hashable, singleton strings.
- If you are using Ruby/Rails on your personal machine and not in a VM, use RVM to install Ruby.
- Make sure you are using a Rails version >= 3.1.
- You need both `Gemfile` and `Gemfile.lock` in your repository.
- If you’re having Gemfile issues on Heroku, run `bundle install` and try again.

In views, note the difference between `<%= 3+4 %>` and `<% 3+4 %>`. The first one evaluates the expression `3+4`, casts the result to a string, and inserts it into the page. The second one merely executes the code and throws away the result. Use the first one for inserting server-generated data into a page; use the second one for control flow constructs like if statements and looping.

If you have extra CSS and JavaScript files, you will have to tell the asset pipeline that you want to compile and serve these files (otherwise it will work in development, but when you deploy on Heroku it will be broken). Here is my solution; it goes in `config/environments/production.rb`:

```
# Precompile additional assets (application.js, application.css, and all non-JS/CSS are already added) extra_assets = Dir.entries("app/assets/stylesheets")+Dir.entries("app/assets/javascripts") extra_assets.delete(".") extra_assets.delete("..") extra_assets.map! { |name| name.gsub(".scss", "").gsub(".coffee", "").gsub(".erb", "") } config.assets.precompile += extra_assets
```

Heroku does not support SQLite, the default Rails database. To push to Heroku, delete the line `gem "sqlite3"` and put this in your `Gemfile` (this will use SQLite locally and PostgreSQL on Heroku):

```
group :production do gem 'pg' end group :development, :test do gem 'sqlite3' end
```

If you have problems installing the `pg` gem on Ubuntu, run `sudo apt-get install libpq-dev` and try again.

If you are using Ubuntu but not the class VM, and your app will not start because you do not have a JavaScript runtime installed, add this to your gemfile: `gem 'therubyracer'`

One last tip: from a view, you may find yourself wanting to insert some HTML into the `<head>` `</head>` tags, such as the page title, or extra JS/CSS includes. To do this:

1. Open `app/views/layouts/application.html` (this is the default layout for all your pages).
2. Add `<%= yield :head %>` somewhere inside the `<head>` `</head>` tags
3. In the view, you can now do something like:

```
<% content_for :head do %> this_will get_inserted_into_the_head_tag <% end %>
```

If you use this for setting the page title, be careful not to set the title twice (once in the layout and once in the view).

You may get the error “uninitialized constant Rake::DSL” when you run: `rake db:migrate`

The problem is that Rake version 0.9.- breaks Rails. Solution: edit the Gemfile to not use this version of Rake. Either works:

- `gem "rake", "0.8.7"`
- `gem "rake", "!=0.9.0"`

Then run: `bundle update rake`
