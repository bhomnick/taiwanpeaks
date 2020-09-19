/*
 * jquery-countTo
 * Copyright (c) 2012-2014 Matt Huggins - The MIT License
 * URL: https://github.com/mhuggins/jquery-countTo/
 */
(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // CommonJS
        factory(require('jquery'));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {
    var CountTo = function (element, options) {
        this.$element = $(element);
        this.options = $.extend({}, CountTo.DEFAULTS, this.dataOptions(), options);
        this.init();
    };

    CountTo.DEFAULTS = {
        from: 0,               // the number the element should start at
        to: 0,                 // the number the element should end at
        speed: 1000,           // how long it should take to count between the target numbers
        refreshInterval: 100,  // how often the element should be updated
        decimals: 0,           // the number of decimal places to show
        formatter: formatter,  // handler for formatting the value before rendering
        onUpdate: null,        // callback method for every time the element is updated
        onComplete: null       // callback method for when the element finishes updating
    };

    CountTo.prototype.init = function () {
        this.value = this.options.from;
        this.loops = Math.ceil(this.options.speed / this.options.refreshInterval);
        this.loopCount = 0;
        this.increment = (this.options.to - this.options.from) / this.loops;
    };

    CountTo.prototype.dataOptions = function () {
        var options = {
            from: this.$element.data('from'),
            to: this.$element.data('to'),
            speed: this.$element.data('speed'),
            refreshInterval: this.$element.data('refresh-interval'),
            decimals: this.$element.data('decimals')
        };

        var keys = Object.keys(options);

        for (var i in keys) {
            var key = keys[i];

            if (typeof (options[key]) === 'undefined') {
                delete options[key];
            }
        }

        return options;
    };

    CountTo.prototype.update = function () {
        this.value += this.increment;
        this.loopCount++;

        this.render();

        if (typeof (this.options.onUpdate) == 'function') {
            this.options.onUpdate.call(this.$element, this.value);
        }

        if (this.loopCount >= this.loops) {
            clearInterval(this.interval);
            this.value = this.options.to;

            if (typeof (this.options.onComplete) == 'function') {
                this.options.onComplete.call(this.$element, this.value);
            }
        }
    };

    CountTo.prototype.render = function () {
        var formattedValue = this.options.formatter.call(this.$element, this.value, this.options);
        this.$element.text(formattedValue);
    };

    CountTo.prototype.restart = function () {
        this.stop();
        this.init();
        this.start();
    };

    CountTo.prototype.start = function () {
        this.stop();
        this.render();
        this.interval = setInterval(this.update.bind(this), this.options.refreshInterval);
    };

    CountTo.prototype.stop = function () {
        if (this.interval) {
            clearInterval(this.interval);
        }
    };

    CountTo.prototype.toggle = function () {
        if (this.interval) {
            this.stop();
        } else {
            this.start();
        }
    };

    function formatter(value, options) {
        return value.toFixed(options.decimals);
    }

    $.fn.countTo = function (option) {
        return this.each(function () {
            var $this = $(this);
            var data = $this.data('countTo');
            var init = !data || typeof (option) === 'object';
            var options = typeof (option) === 'object' ? option : {};
            var method = typeof (option) === 'string' ? option : 'start';

            if (init) {
                if (data) data.stop();
                $this.data('countTo', data = new CountTo(this, options));
            }

            data[method].call(data);
        });
    };
}));

/*
* ===========================================================
* PROGRESS BAR - CIRCLE PROGRESS BAR - COUNTER - COUNTDOWN - THEMEKIT
* ===========================================================
* This script manage the following component: progress bar, circle progress bar, counter and countdown.
* 
* Copyright (c) Federico Schiocchet - schiocco.com - Themekit
*/

(function ($) {
    $.fn.init_progress_all = function () {
        var t = this;
        $(t).find("[data-time]").each(function () {
            $(this).progressCountdown();
        });
        $(window).scroll(function () {
            $(t).find("[data-to]").each(function () {
                if (isScrollView(this)) {
                    var trigger = $(this).attr("data-trigger");
                    if (isEmpty(trigger) || trigger == "scroll") {
                        $(this).progressCounter();
                    }
                }
            });
            $(t).find(".progress-bar").each(function () {
                if (isScrollView(this)) {
                    var trigger = $(this).attr("data-trigger");
                    if (isEmpty(trigger) || trigger == "scroll") {
                        $(this).find("[data-progress]").progressBar();
                    }
                }
            });
            $(t).find(".progress-circle").each(function () {
                if (isScrollView(this)) {
                    var trigger = $(this).attr("data-trigger");
                    if (isEmpty(trigger) || trigger == "scroll") {
                        $(this).progressCircle();
                    }
                }
            });
        })
    }
    $.fn.progressCountdown = function () {
        var date = $(this).attr("data-time");
        if (!isEmpty(date)) {
            $(this).downCount({
                date: date,
                offset: $(this).attr("data-utc-offset")
            });
        }
    }
    $.fn.progressCounter = function () {
        var separator = $(this).attr("data-separator");
        var unit = $(this).attr("data-unit");
        if (separator == null) separator = "";
        if (unit == null) unit = "";
        else unit = " " + unit;
        $(this).countTo({
            formatter: function (value, options) {
                return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, separator) + unit;
            }
        });
        $(this).attr("data-trigger", "null");
    }
    $.fn.progressBar = function () {
        $(this).css("width", 0);
        $(this).css("width", $(this).attr("data-progress") + "%");
        $(this).attr("data-trigger", "null");
    }
    $.fn.progressCircle = function () {
        var optionsArr;
        var optionsString = $(this).attr("data-options");
        var window_width = $(window).width();
        var size = $(this).attr("data-size");
        var color = $(this).attr("data-color");
        var unit = $(this).attr("data-unit");
        var thickness = $(this).attr("data-thickness");
        var lineCap = $(this).attr("data-linecap");
        if (isEmpty(color)) color = "#565656";
        if (isEmpty(thickness)) thickness = 2;
        if (unit == null) unit = "%";
        if (window_width < 994) {
            size = $(this).attr("data-size-md");
        }
        if (window_width < 768) {
            size = $(this).attr("data-size-sm");
        }
        if (isEmpty(size) || size == "auto") size = $(this).outerWidth();
        if (isEmpty(size)) size = $(this).parent().width();
        if (isEmpty(size)) size = $(this).attr("data-size");

        var options = {
            value: parseInt($(this).attr("data-progress"), 10) / 100,
            size: size,
            lineCap: lineCap,
            fill: {
                gradient: [color, color]
            },
            thickness: thickness,
            startAngle: -Math.PI / 2
        }
        if (!isEmpty(optionsString)) {
            optionsArr = optionsString.split(",");
            options = getOptionsString(optionsString, options);
        }
        $(this).circleProgress(options);
        $(this).attr("data-trigger", "null");
    }
}(jQuery));