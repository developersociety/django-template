/* global require */

var gulp = require("gulp");
var sourcemaps = require("gulp-sourcemaps");
var pump = require("pump");
var argv = require("yargs-parser")(process.argv.slice(2));

// CSS processors
var sass = require("gulp-sass");

// Post CSS transformations
var postcss = require("gulp-postcss");
var atImport = require("postcss-import");
var autoprefixer = require("autoprefixer");
var cssnano = require("cssnano");

// Browser auto refresh/reload
var browserSync = require("browser-sync").create();

gulp.task("sass", function(cb) {
    "use strict";

    var processors = [atImport(), autoprefixer()];

    if (argv.production === true) {
        processors.push(cssnano());
    }

    pump(
        [
            gulp.src(["./static/scss/*.scss", "!**/_*.scss"]),
            sourcemaps.init(),
            sass({
                includePaths: ["node_modules/normalize-scss/sass"]
            }),
            postcss(processors),
            sourcemaps.write("."),
            gulp.dest("./static/css"),
            browserSync.stream({ match: "**/*.css" })
        ],
        cb
    );
});

gulp.task("default", ["sass"]);

gulp.task("serve", ["default"], function() {
    "use strict";

    // Adjust ports based on what Django is using
    var django_ip = process.env.DJANGO_IP || "127.0.0.1";
    var django_port = parseInt(process.env.DJANGO_PORT || 8000);
    var browsersync_port = django_port + 1;
    var browsersyncui_port = django_port + 2;

    // Tweak log level if needed
    var loglevel = "info";
    if (argv.silent === true) {
        loglevel = "silent";
    }

    browserSync.init({
        host: django_ip,
        port: browsersync_port,
        ui: {
            port: browsersyncui_port
        },
        browser: [],
        logSnippet: false,
        logLevel: loglevel
    });

    gulp.watch("./static/scss/**/*", ["sass"]);
});
