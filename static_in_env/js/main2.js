"use strict";
// $(window).scroll(function() {

//     if ($(this).scrollTop() > 400)
//      {
//         $('.scroll-hide').fadeOut();
//      }
//     else
//      {
//       $('.scroll-hide').fadeIn();
//      }
//  });
//  $(window).scroll(function() {
//     if ($(this).scrollTop() > 400)
//      {
//         $('.scroll-show').show();
//         $('.product-sticky-content').removeClass('d-none d-lg-block d-xl-none')
//     }
//     else
//     {
//         $('.scroll-show').hide();
//         $('.product-sticky-content').addClass('d-none d-lg-block d-xl-none')
//      }
//  });
// var navShown = false;

// $(window).scroll(function() {
//     var currentScrollPos = $(this).scrollTop();
    
//     if (!navShown && currentScrollPos > 400) {
//         // Show the navigation
//         $('.scroll-show').show();
//         $('.product-sticky-content').removeClass('d-none d-lg-block d-xl-none');
//         navShown = true;
//     } else if (navShown && currentScrollPos <= 20) {
//         // Hide the navigation
//         $('.scroll-show').hide();
//         $('.product-sticky-content').addClass('d-none d-lg-block d-xl-none');
//         navShown = false;
//     }
// });
 var mobile = (/iphone|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));  
    if(mobile) {
        $('.navWrap').hide();
    }
var $ = jQuery.noConflict();
$.extend($.easing, {
    def: "easeOutQuad",
    swing: function (e, t, i, o, n) {
        return $.easing[$.easing.def](e, t, i, o, n);
    },
    easeOutQuad: function (e, t, i, o, n) {
        return -o * (t /= n) * (t - 2) + i;
    },
    easeOutQuint: function (e, t, i, o, n) {
        return o * ((t = t / n - 1) * t * t * t * t + 1) + i;
    },
}),
    (window.Riode = {}),
    (Riode.$window = $(window)),
    (Riode.$body = $(document.body)),
    (Riode.status = ""),
    (Riode.minDesktopWidth = 992),
    (Riode.isIE = navigator.userAgent.indexOf("Trident") >= 0),
    (Riode.isEdge = navigator.userAgent.indexOf("Edge") >= 0),
    (Riode.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)),
    (Riode.defaults = {
        animation: { name: "fadeIn", duration: "1.2s", delay: ".2s" },
        isotope: { itemsSelector: ".grid-item", layoutMode: "masonry", percentPosition: !0, masonry: { columnWidth: ".grid-space" } },
        minipopup: {
            message: "",
            productClass: "",
            imageSrc: "",
            imageLink: "#",
            name: "",
            nameLink: "#",
            price: "",
            count: null,
            rating: null,
            actionTemplate: "",
            isPurchased: !1,
            delay: 4e3,
            space: 20,
            priceTemplate: '<span class="product-price">{{price}}</span>',
            ratingTemplate: '<div class="ratings-container"><div class="ratings-full"><span class="ratings" style="width:{{rating}}"></span><span class="tooltiptext tooltip-top"></span></div></div>',
            priceQuantityTemplate: '<div class="price-box"><span class="product-quantity">{{count}}</span><span class="product-price">{{price}}</span></div>',
            purchasedTemplate: '<span class="purchased-time">12 MINUTES AGO</span>',
            template:
                '<div class="minipopup-box"><p class="minipopup-title">{{message}}</p><div class="product product-purchased {{productClass}} mb-0"><figure class="product-media"><a href="{{imageLink}}"><img src="{{imageSrc}}" alt="product" width="90" height="90"></a></figure><div class="product-detail"><a href="{{nameLink}}" class="product-name">{{name}}</a>{{detailTemplate}}</div></div>{{actionTemplate}}</div>',
        },
        popup: {
            removalDelay: 350,
            callbacks: {
                open: function () {
                    $("html").css("overflow-y", "hidden"), $("body").css("overflow-x", "visible"), $(".mfp-wrap").css("overflow", "hidden auto"), $(".sticky-header.fixed").css("padding-right", window.innerWidth - document.body.clientWidth);
                },
                close: function () {
                    $("html").css("overflow-y", ""), $("body").css("overflow-x", "hidden"), $(".mfp-wrap").css("overflow", ""), $(".sticky-header.fixed").css("padding-right", "");
                },
            },
        },
        popupPresets: {
            login: { type: "ajax", mainClass: "mfp-login mfp-fade", tLoading: "", preloader: !1 },
            video: { type: "iframe", mainClass: "mfp-fade", preloader: !1, closeBtnInside: !1 },
            quickview: { type: "ajax", mainClass: "mfp-product mfp-fade", tLoading: "", preloader: !1 },
        },
        slider: {
            responsiveClass: !0,
            navText: ['<i class="d-icon-angle-left">', '<i class="d-icon-angle-right">'],
            checkVisible: !1,
            items: 1,
            smartSpeed: Riode.isEdge ? 200 : 500,
            autoplaySpeed: Riode.isEdge ? 200 : 1e3,
            autoplayTimeout: 1e4,
        },
        sliderPresets: {
            "intro-slider": { animateIn: "fadeIn", animateOut: "fadeOut" },
            "product-single-carousel": { dots: !1, nav: !0 },
            "product-gallery-carousel": { dots: !1, nav: !0, margin: 0, items: 1, responsive: { 576: { items: 2 }, 768: { items: 4 } } },
            "rotate-slider": { dots: !1, nav: !0, margin: 0, items: 1, animateIn: "", animateOut: "" },
        },
        sliderThumbs: { margin: 0, items: 4, dots: !1, nav: !0, navText: ['<i class="fas fa-chevron-left">', '<i class="fas fa-chevron-right">'] },
        stickyContent: { minWidth: Riode.minDesktopWidth, maxWidth: 2e4, top: 300, hide: !1, max_index: 1060, scrollMode: !1 },
        stickyHeader: { activeScreenWidth: 768 },
        stickyFooter: { minWidth: 0, maxWidth: 767, top: 150, hide: !0, scrollMode: !0 },
        stickyToolbox: { minWidth: 0, maxWidth: 767, top: !1, scrollMode: !0 },
        stickySidebar: { autoInit: !0, minWidth: 991, containerSelector: ".sticky-sidebar-wrapper", autoFit: !0, activeClass: "sticky-sidebar-fixed", paddingOffsetTop: 93, paddingOffsetBottom: 0 },
        templateCartAddedAlert:
            '<div class="alert alert-simple alert-btn cart-added-alert"><a href="/panier" class="btn btn-success btn-md">View Cart</a><span>"{{name}}" has been added to your cart.</span><button type="button" class="btn btn-link btn-close"><i class="d-icon-times"></i></button></div>',
        zoomImage: { responsive: !0, zoomWindowFadeIn: 750, zoomWindowFadeOut: 500, borderSize: 0, zoomType: "inner", cursor: "crosshair" },
    }),
    (Riode.$ = function (e) {
        return e instanceof jQuery ? e : $(e);
    }),
    (Riode.call = function (e, t) {
        setTimeout(e, t);
    }),
    (Riode.byId = function (e) {
        return document.getElementById(e);
    }),
    (Riode.byTag = function (e, t) {
        return t ? t.getElementsByTagName(e) : document.getElementsByTagName(e);
    }),
    (Riode.byClass = function (e, t) {
        return t ? t.getElementsByClassName(e) : document.getElementsByClassName(e);
    }),
    (Riode.setCookie = function (e, t, i) {
        var o = new Date();
        o.setTime(o.getTime() + 24 * i * 60 * 60 * 1e3), (document.cookie = e + "=" + t + ";expires=" + o.toUTCString() + ";path=/");
    }),
    (Riode.getCookie = function (e) {
        for (var t = e + "=", i = document.cookie.split(";"), o = 0; o < i.length; ++o) {
            for (var n = i[o]; " " == n.charAt(0); ) n = n.substring(1);
            if (0 == n.indexOf(t)) return n.substring(t.length, n.length);
        }
        return "";
    }),
    (Riode.parseOptions = function (e) {
        return "string" == typeof e ? JSON.parse(e.replace(/'/g, '"').replace(";", "")) : {};
    }),
    (Riode.parseTemplate = function (e, t) {
        return e.replace(/\{\{(\w+)\}\}/g, function () {
            return t[arguments[1]];
        });
    }),
    (Riode.isOnScreen = function (e, t, i) {
        var o = window.pageXOffset,
            n = window.pageYOffset,
            a = e.getBoundingClientRect(),
            s = a.left + o,
            d = a.top + n,
            r = void 0 === t ? 0 : t,
            l = void 0 === i ? 0 : i;
        return d + a.height + l >= n && d <= n + window.innerHeight + l && s + a.width + r >= o && s <= o + window.innerWidth + r;
    }),
    (Riode.initTab = function (e) {
        Riode.$body
            .on("click", ".tab .nav-link", function (e) {
                var t = $(this);
                console.log('oui');
                if ((e.preventDefault(), !t.hasClass("active"))) {
                    var i = $(t.attr("href"));
                    i.siblings().removeClass("in active"), i.addClass("active in"), Riode.slider(i.find(".owl-carousel")), t.parent().parent().find(".active").removeClass("active"), t.addClass("active");
                }
            })
            .on("click", ".link-to-tab", function (e) {
                var t = $(e.currentTarget).attr("href"),
                    i = $(t),
                    o = i.parent().siblings(".nav");
                e.preventDefault(),
                    i.siblings().removeClass("active in"),
                    i.addClass("active in"),
                    o.find(".nav-link").removeClass("active"),
                    o.find('[href="' + t + '"]').addClass("active"),
                    $("html").animate({ scrollTop: i.offset().top - 150 });
            });
    }),
    (Riode.appear = (function () {
        var e,
            t = [],
            i = !1,
            o = function () {
                for (var i = t.length; i--; )
                    (e = t[i]),
                        Riode.isOnScreen(e.el, e.options.accX, e.options.accY) && ("function" == typeof $(e.el).data("appear-callback") && $(e.el).data("appear-callback").call(e.el, e.data), e.fn && e.fn.call(e.el, e.data), t.splice(i, 1));
            };
        return (
            window.addEventListener("scroll", o, { passive: !0 }),
            window.addEventListener("resize", o, { passive: !0 }),
            $(window).on("appear.check", o),
            function (e, n, a) {
                var s = { data: void 0, accX: 0, accY: 0 };
                a && (a.data && (s.data = a.data), a.accX && (s.accX = a.accX), a.accY && (s.accY = a.accY)), t.push({ el: e, fn: n, options: s }), i || (i = Riode.requestTimeout(o, 100));
            }
        );
    })()),
    (Riode.zoomImageObjects = []),
    (Riode.zoomImage = function (e) {
        $.fn.elevateZoom &&
            e &&
            Riode.$(e)
                .find("img")
                .each(function () {
                    var e = $(this);
                    (Riode.defaults.zoomImage.zoomContainer = e.parent()), e.elevateZoom(Riode.defaults.zoomImage), Riode.zoomImageObjects.push(e);
                });
    }),
    (Riode.initZoom = function () {
        window.addEventListener(
            "resize",
            function () {
                Riode.zoomImageObjects.forEach(function (e) {
                    e.each(function () {
                        var e = $(this).data("elevateZoom");
                        e && e.refresh();
                    });
                });
            },
            { passive: !0 }
        );
    }),
    (Riode.countTo = function (e) {
        $.fn.countTo &&
            Riode.$(e).each(function () {
                Riode.appear(this, function () {
                    var e = $(this);
                    setTimeout(function () {
                        e.countTo({
                            onComplete: function () {
                                e.addClass("complete");
                            },
                        });
                    }, 300);
                });
            });
    }),
    (Riode.countdown = function (e) {
        $.fn.countdown &&
            Riode.$(e).each(function () {
                var e = $(this),
                    t = e.data("until"),
                    i = e.data("compact"),
                    o = e.data("format") ? e.data("format") : "DHMS",
                    n = e.data("labels-short") ? ["Years", "Months", "Weeks", "Days", "Hours", "Mins", "Secs"] : ["Years", "Months", "Weeks", "Days", "Hours", "Minutes", "Seconds"],
                    a = e.data("labels-short") ? ["Year", "Month", "Week", "Day", "Hour", "Min", "Sec"] : ["Year", "Month", "Week", "Day", "Hour", "Minute", "Second"];
                if (e.data("relative")) d = t;
                else
                    var s = t.split(", "),
                        d = new Date(s[0], s[1] - 1, s[2]);
                e.countdown({ until: d, format: o, padZeroes: !0, compact: i, compactLabels: [" y", " m", " w", " days, "], timeSeparator: " : ", labels: n, labels1: a });
            });
    }),
    (Riode.priceSlider = function (e, t) {
        "object" == typeof noUiSlider &&
            Riode.$(e).each(function () {
                var e = this;
                noUiSlider.create(e, $.extend(!0, { start: [18, 35], connect: !0, step: 1, range: { min: 18, max: 35 } }, t)),
                    e.noUiSlider.on("update", function (t, i) {
                        t = t.map(function (e) {
                            return "$" + parseInt(e);
                        });
                        $(e).parent().find(".filter-price-range").text(t.join(" - "));
                    });
            });
    }),
    (Riode.lazyload = function (e, t) {
        function i() {
            this.setAttribute("src", this.getAttribute("data-src")),
                this.addEventListener("load", function () {
                    (this.style["padding-top"] = ""), this.classList.remove("lazy-img");
                });
        }
        Riode.$(e)
            .find(".lazy-img")
            .each(function () {
                void 0 !== t && t ? i.call(this) : Riode.appear(this, i);
            });
    }),
    (Riode.isotopes = function (e, t) {
        if ("function" == typeof imagesLoaded && $.fn.isotope) {
            Riode.$(e).each(function () {
                var e = $(this),
                    i = $.extend(!0, {}, Riode.defaults.isotope, Riode.parseOptions(e.attr("data-grid-options")), t || {});
                Riode.lazyload(e),
                    e.imagesLoaded(function () {
                        i.customInitHeight && e.height(e.height()),
                            i.customDelay &&
                                Riode.call(function () {
                                    e.isotope(i);
                                }, parseInt(i.customDelay)),
                            e.isotope(i);
                    });
            });
        }
    }),
    (Riode.initNavFilter = function (e) {
        $.fn.isotope &&
            Riode.$(e).on("click", function (e) {
                var t = $(this),
                    i = t.attr("data-filter"),
                    o = t.parent().parent().attr("data-target");
                $(o ? o : ".grid")
                    .isotope({ filter: i })
                    .isotope("on", "arrangeComplete", function () {
                        Riode.$window.trigger("appear.check");
                    }),
                    t.parent().siblings().children().removeClass("active"),
                    t.addClass("active"),
                    e.preventDefault();
            });
    }),
    (Riode.initShowVendorSearch = function (e) {
        Riode.$body.on("click", e, function (e) {
            var t = $(this).closest(".toolbox").next(".form-wrapper");
            t.hasClass("open") ? t.slideUp().removeClass("open") : t.slideDown().addClass("open"), e.preventDefault();
        });
    }),
    (Riode.parallax = function (e, t) {
        $.fn.themePluginParallax &&
            Riode.$(e).each(function () {
                var e = $(this);
                e.themePluginParallax($.extend(!0, Riode.parseOptions(e.attr("data-parallax-options")), t));
            });
    }),
    (Riode.headerToggleSearch = function (e) {
        var t = Riode.$(e);
        t
            .find(".form-control")
            .on("focusin", function (e) {
                t.addClass("show");
            })
            .on("focusout", function (e) {
                t.removeClass("show");
            }),
            Riode.$body.on("click", ".sticky-footer .search-toggle", function (e) {
                $(this).parent().toggleClass("show"), e.preventDefault();
            });
    }),
    (Riode.closeTopNotice = function (e) {
        var t = Riode.$(e);
        t.on("click", function (e) {
            e.preventDefault(), t.closest(".top-notice").css("display", "none");
        });
    }),
    (Riode.stickyHeader = function (e) {
        var t = Riode.$(e);
        if (0 != t.length) {
            var i,
                o,
                n = !1,
                a = function () {
                    if (((i = t[0].offsetHeight), (o = t.offset().top + i), t.hasClass("has-dropdown"))) {
                        t.find(".category-dropdown .dropdown-box").length && (o += t.find(".category-dropdown .dropdown-box")[0].offsetHeight);
                    }
                    !n && window.innerWidth >= Riode.defaults.stickyHeader.activeScreenWidth && ((n = !0), t.wrap('<div class="sticky-wrapper" style="height:' + i + 'px"></div>')), Riode.$window.off("resize", a);
                },
                s = function () {
                    window.innerWidth >= Riode.defaults.stickyHeader.activeScreenWidth && window.pageYOffset >= o
                        ? (t[0].classList.add("fixed"), document.body.classList.add("sticky-header-active"))
                        : (t[0].classList.remove("fixed"), document.body.classList.remove("sticky-header-active"));
                };
            window.addEventListener("scroll", s, { passive: !0 }), Riode.$window.on("resize", a), Riode.$window.on("resize", s), Riode.call(a, 500), Riode.call(s, 500);
        }
    }),
    (Riode.stickyContent = function (e, t) {
        var i = Riode.$(e),
            o = $.extend({}, Riode.defaults.stickyContent, t),
            n = window.pageYOffset;
        if (0 != i.length) {
            var a = function () {
                    i.each(function (e) {
                        var t = $(this);
                        if (t.data("is-wrap")) (window.innerWidth < o.minWidth || window.innerWidth >= o.maxWidth) && (t.unwrap(".sticky-content-wrapper"), t.data("is-wrap", !1));
                        else {
                            var i,
                                n = t.removeClass("fixed").outerHeight(!0);
                            if (((i = t.offset().top + n), t.hasClass("has-dropdown"))) {
                                var a = t.find(".category-dropdown .dropdown-box");
                                a.length && (i += a[0].offsetHeight);
                            }
                            t.data("top", i),
                                (function (e, t) {
                                    window.innerWidth >= o.minWidth && window.innerWidth <= o.maxWidth && (e.wrap('<div class="sticky-content-wrapper"></div>'), e.parent().css("height", t + "px"), e.css("display", "none"), e.data("is-wrap", !0));
                                })(t, n);
                        }
                    });
                },
                s = function (e) {
                    (e && !e.isTrusted) ||
                        i.each(function (e) {
                            var t = $(this),
                                i = !0;
                            o.scrollMode && ((i = n > window.pageYOffset), (n = window.pageYOffset)),
                                window.pageYOffset > (0 == o.top ? t.data("top") : o.top) && window.innerWidth >= o.minWidth && window.innerWidth <= o.maxWidth
                                    ? (t.hasClass("fix-top")
                                          ? (void 0 === t.data("offset-top") &&
                                                (function (e) {
                                                    var t = 0,
                                                        i = 0;
                                                    $(".sticky-content.fixed.fix-top").each(function () {
                                                        console.log('thisss', $(this)[0]);
                                                        (t += $(this)[0].offsetHeight), i++;

                                                    }),
                                                        e.data("offset-top", t),
                                                        e.data("z-index", o.max_index - i);
                                                })(t),
                                            t.css("margin-top", t.data("offset-top") + "px"))
                                          : t.hasClass("fix-bottom") &&
                                            (void 0 === t.data("offset-bottom") &&
                                                (function (e) {
                                                    var t = 0,
                                                        i = 0;
                                                    $(".sticky-content.fixed.fix-bottom").each(function () {
                                                        (t += $(this)[0].offsetHeight), i++;
                                                    }),
                                                        e.data("offset-bottom", t),
                                                        e.data("z-index", o.max_index - i);
                                                })(t),
                                            t.css("margin-bottom", t.data("offset-bottom") + "px")),
                                      t.css("z-index", t.data("z-index")),
                                      o.scrollMode ? ((i && t.hasClass("fix-top")) || (!i && t.hasClass("fix-bottom")) ? (t.addClass("fixed"), t.removeClass("d-none") ): (t.addClass("d-none"), t.css("margin", ""))) : t.addClass("fixed"),
                                      o.hide && t.parent(".sticky-content-wrapper").css("display", ""))
                                    : (t.removeClass("fixed"), t.css("margin-top", ""), t.css("margin-bottom", ""), o.hide && t.parent(".sticky-content-wrapper").css("display", "none"));
                        });
                },
                d = function (e) {
                    i.removeData("offset-top").removeData("offset-bottom").removeClass("fixed").css("margin", "").css("z-index", ""),
                        Riode.call(function () {
                            a(), s();
                        });
                };
            setTimeout(a, 550),
                setTimeout(s, 600),
                Riode.call(function () {
                    window.addEventListener("scroll", s, { passive: !0 }), Riode.$window.on("resize", d);
                }, 700);
        }
    }),
    (Riode.initAlert = function (e) {
        Riode.$body.on("click", e + " .btn-close", function (t) {
            $(this)
                .closest(e)
                .fadeOut(function () {
                    $(this).remove();
                });
        });
    }),
    (Riode.initAccordion = function (e) {
        Riode.$body.on("click", e, function (e) {
            var i = $(this),
                o = i.closest(".card").find(i.attr("href")),
                n = i.closest(".accordion");
            e.preventDefault(),
                0 === n.find(".collapsing").length &&
                    0 === n.find(".expanding").length &&
                    (o.hasClass("expanded")
                        ? n.hasClass("radio-type") || t(o)
                        : o.hasClass("collapsed") &&
                          (n.find(".expanded").length > 0
                              ? Riode.isIE
                                  ? t(n.find(".expanded"), function () {
                                        t(o);
                                    })
                                  : (t(n.find(".expanded")), t(o))
                              : t(o)));
        });
        var t = function (t, i) {
            var o = t.closest(".card").find(e);
            t.hasClass("expanded")
                ? (o.removeClass("collapse").addClass("expand"),
                  t.addClass("collapsing").slideUp(300, function () {
                      t.removeClass("expanded collapsing").addClass("collapsed"), i && i();
                  }))
                : t.hasClass("collapsed") &&
                  (o.removeClass("expand").addClass("collapse"),
                  t.addClass("expanding").slideDown(300, function () {
                      t.removeClass("collapsed expanding").addClass("expanded"), i && i();
                  }));
        };
    }),


    (Riode.playableVideo = function (e) {
        $(e + " .video-play").on("click", function (t) {
            var i = $(this).closest(e);
            i.hasClass("playing") ? i.removeClass("playing").addClass("paused").find("video")[0].pause() : i.removeClass("paused").addClass("playing").find("video")[0].play(), t.preventDefault();
        }),
            $(e + " video").on("ended", function () {
                $(this).closest(e).removeClass("playing");
            });
    }),
    (Riode.appearAnimate = function (e) {
        Riode.$(e).each(function () {
            var e = this;
            Riode.appear(e, function () {
                if (e.classList.contains("appear-animate")) {
                    var t = $.extend({}, Riode.defaults.animation, Riode.parseOptions(e.getAttribute("data-animation-options")));
                    Riode.call(function () {
                        setTimeout(
                            function () {
                                (e.style["animation-duration"] = t.duration), e.classList.add(t.name), e.classList.add("appear-animation-visible");
                            },
                            t.delay ? 1e3 * Number(t.delay.slice(0, -1)) : 0
                        );
                    });
                }
            });
        });
    }),
    (Riode.stickySidebar = function (e) {
        $.fn.themeSticky &&
            Riode.$(e).each(function () {
                var e = $(this);
                e.themeSticky($.extend(Riode.defaults.stickySidebar, Riode.parseOptions(e.attr("data-sticky-options")))), e.trigger("recalc.pin");
            });
    }),
    (Riode.refreshSidebar = function (e) {
        $.fn.themeSticky &&
            Riode.$(e).each(function () {
                $(this).trigger("recalc.pin");
            });
    }),
    (Riode.ratingTooltip = function (e) {
        for (
            var t = Riode.byClass("ratings-full", e || document.body),
                i = t.length,
                o = function () {
                    var e = parseInt(this.firstElementChild.style.width.slice(0, -1)) / 20;
                    this.lastElementChild.innerText = e ? e.toFixed(2) : e;
                },
                n = 0;
            n < i;
            ++n
        )
            t[n].addEventListener("mouseover", o), t[n].addEventListener("touchstart", o);
    }),
    (Riode.popup = function (e, t) {
        var i = $.magnificPopup.instance,
            o = $.extend(!0, {}, Riode.defaults.popup, void 0 !== t ? Riode.defaults.popupPresets[t] : {}, e);
        i.isOpen && i.content
            ? (i.close(),
              setTimeout(function () {
                  $.magnificPopup.open(o);
              }, 500))
            : $.magnificPopup.open(o);
    }),
    (Riode.initPopups = function () {
        Riode.$body
            .on("click", "a.login, .login-link", function (e) {
                e.preventDefault(), Riode.popup({ items: { src: $(e.currentTarget).attr("href") } }, "login");
            })
            .on("click", ".register-link", function (e) {
                e.preventDefault(),
                    Riode.popup(
                        {
                            items: { src: $(e.currentTarget).attr("href") },
                            callbacks: {
                                ajaxContentAdded: function () {
                                    this.wrap.find('[href="#register"]').click();
                                },
                            },
                        },
                        "login"
                    );
            })
            .on("click", ".btn-iframe", function (e) {
                e.preventDefault(), Riode.popup({ items: { src: '<video src="' + $(e.currentTarget).attr("href") + '" autoplay loop controls>', type: "inline" }, mainClass: "mfp-video-popup" }, "video");
            }),
            $("#newsletter-popup").length > 0 &&
                "true" !== Riode.getCookie("hideNewsletterPopup") &&
                setTimeout(function () {
                    Riode.popup({
                        items: { src: "#newsletter-popup" },
                        type: "inline",
                        tLoading: "",
                        mainClass: "mfp-newsletter mfp-flip-popup",
                        callbacks: {
                            beforeClose: function () {
                                $("#hide-newsletter-popup")[0].checked && Riode.setCookie("hideNewsletterPopup", !0, 7);
                            },
                        },
                    });
                }, 7500);
    }),
    // (Riode.initPurchasedMinipopup = function () {
    //     setInterval(function () {
    //         Riode.Minipopup.open({ message: "Someone Purchased", productClass: "product-cart", name: "Daisy Shoes Sonia by Sonia-Blue", nameLink: "product.html", imageSrc: "images/cart/product-1.jpg", isPurchased: !0 }, function (e) {
    //             Riode.ratingTooltip(e[0]);
    //         });
    //     }, 6e4);
    // }),

    (Riode.initScrollTopButton = function () {
        var e = Riode.byId("scroll-top");
        if (e) {
            e.addEventListener("click", function (e) {
                $("html, body").animate({ scrollTop: 0 }, 600), e.preventDefault();
            });
            var t = function () {
                window.pageYOffset > 400 ? e.classList.add("show") : e.classList.remove("show");
            };
            Riode.call(t, 500), window.addEventListener("scroll", t, { passive: !0 });
        }
    }),
    (Riode.requestTimeout = function (e, t) {
        function i(s) {
            n || (n = s);
            s - n >= t ? e() : (a.val = o(i));
        }
        var o = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame;
        if (!o) return setTimeout(e, t);
        var n,
            a = new Object();
        return (a.val = o(i)), a;
    }),
    (Riode.requestInterval = function (e, t, i) {
        function o(r) {
            a || (a = s = r);
            !i || r - a < i ? (r - s > t ? ((d.val = n(o)), e(), (s = r)) : (d.val = n(o))) : e();
        }
        var n = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame;
        if (!n) return i ? setInterval(e, t) : setTimeout(e, i);
        var a,
            s,
            d = new Object();
        return (d.val = n(o)), d;
    }),
    (Riode.deleteTimeout = function (e) {
        if (e) {
            var t = window.cancelAnimationFrame || window.webkitCancelAnimationFrame || window.mozCancelAnimationFrame;
            return t ? (e.val ? t(e.val) : void 0) : clearTimeout(e);
        }
    }),
    (Riode.sidebar = (function () {
        function e(e) {
            return this.init(e);
        }
        var t = window.innerWidth < Riode.minDesktopWidth,
            i = function () {
                window.innerWidth < Riode.minDesktopWidth && !t
                    ? (this.$sidebar.find(".sidebar-content, .filter-clean").removeAttr("style"),
                      this.$sidebar.find(".sidebar-content").attr("style", ""),
                      this.$sidebar.siblings(".toolbox").children(":not(:first-child)").removeAttr("style"))
                    : window.innerWidth >= Riode.minDesktopWidth && !this.$sidebar.hasClass("closed") && t && (this.$sidebar.addClass("closed"), this.$sidebar.find(".sidebar-content").css("display", "none")),
                    (t = window.innerWidth < Riode.minDesktopWidth);
            };
        return (
            (e.prototype.init = function (e) {
                var t = this;
                return (
                    (t.name = e),
                    (t.$sidebar = $("." + e)),
                    (t.isNavigation = !1),
                    t.$sidebar.length &&
                        ((t.isNavigation = t.$sidebar.hasClass("sidebar-fixed") && t.$sidebar.parent().hasClass("toolbox-wrap")),
                        t.isNavigation && ((i = i.bind(this)), Riode.$window.on("resize", i)),
                        Riode.$window.on("resize", function () {
                            Riode.$body.removeClass(e + "-active");
                        }),
                        t.$sidebar
                            .find(".sidebar-toggle, .sidebar-toggle-btn")
                            .add("sidebar" === e ? ".left-sidebar-toggle" : "." + e + "-toggle")
                            .on("click", function (e) {
                                t.toggle(), $(this).blur(), $(".sticky-sidebar").trigger("recalc.pin.left", [400]), e.preventDefault();
                            }),
                        t.$sidebar.find(".sidebar-overlay, .sidebar-close").on("click", function (t) {
                            Riode.$body.removeClass(e + "-active"), $(".sticky-sidebar").trigger("recalc.pin.left", [400]), t.preventDefault();
                        }),
                        setTimeout(function () {
                            $(".sticky-sidebar").trigger("recalc.pin", [400]);
                        })),
                    !1
                );
            }),
            (e.prototype.toggle = function () {
                var e = this;
                if (window.innerWidth >= Riode.minDesktopWidth && e.$sidebar.hasClass("sidebar-fixed")) {
                    var t = e.$sidebar.hasClass("closed");
                    if (
                        (e.isNavigation &&
                            (t || e.$sidebar.find(".filter-clean").hide(),
                            e.$sidebar.siblings(".toolbox").children(":not(:first-child)").fadeToggle("fast"),
                            e.$sidebar
                                .find(".sidebar-content")
                                .stop()
                                .animate({ height: "toggle", "margin-bottom": t ? "toggle" : -6 }, function () {
                                    $(this).css("margin-bottom", ""), t && e.$sidebar.find(".filter-clean").fadeIn("fast");
                                })),
                        e.$sidebar.hasClass("shop-sidebar"))
                    ) {
                        var i = $(".main-content .product-wrapper");
                        if (i.length)
                            if (i.hasClass("product-lists")) i.toggleClass("row cols-xl-2", !t);
                            else {
                                var o = i.data("toggle-cols"),
                                    n = i.attr("class").match(/cols-\w*-*\d/g),
                                    a = n
                                        ? Math.max.apply(
                                              null,
                                              n.map(function (e) {
                                                  return e.match(/\d/)[0];
                                              })
                                          )
                                        : 0;
                                t ? 4 === a && 3 == o && i.removeClass("cols-md-4") : 3 === a && (i.addClass("cols-md-4"), o || i.data("toggle-cols", 3));
                            }
                    }
                    e.$sidebar.toggleClass("closed");
                } else
                    e.$sidebar.find(".sidebar-overlay .sidebar-close").css("margin-left", -(window.innerWidth - document.body.clientWidth)),
                        Riode.$body.toggleClass(e.name + "-active").removeClass("closed"),
                        window.innerWidth >= 1200 && Riode.$body.hasClass("with-flex-container") && $(".owl-carousel").trigger("refresh.owl.carousel");
            }),
            function (t) {
                return new e(t);
            }
        );
    })()),
    (Riode.initProductSingle = (function () {
        function e(e) {
            return this.init(e);
        }
        var t = function (e) {
                var t = e.$thumbsWrap.offset().top + e.$thumbsWrap[0].offsetHeight,
                    i = e.$thumbs.offset().top + e.thumbsHeight;
                i >= t + e.$productThumb[0].offsetHeight
                    ? (e.$thumbs.css("top", parseInt(e.$thumbs.css("top")) - e.$productThumb[0].offsetHeight), e.$thumbUp.removeClass("disabled"))
                    : i > t
                    ? (e.$thumbs.css("top", parseInt(e.$thumbs.css("top")) - Math.ceil(i - t)), e.$thumbUp.removeClass("disabled"), e.$thumbDown.addClass("disabled"))
                    : e.$thumbDown.addClass("disabled");
            },
            i = function (e) {
                var t = e.$thumbsWrap.offset().top,
                    i = e.$thumbs.offset().top;
                i <= t - e.$productThumb[0].offsetHeight
                    ? (e.$thumbs.css("top", parseInt(e.$thumbs.css("top")) + e.$productThumb[0].offsetHeight), e.$thumbDown.removeClass("disabled"))
                    : i < t
                    ? (e.$thumbs.css("top", parseInt(e.$thumbs.css("top")) - Math.ceil(i - t)), e.$thumbDown.removeClass("disabled"), e.$thumbUp.addClass("disabled"))
                    : e.$thumbUp.addClass("disabled");
            },
            o = function (e) {
                if (void 0 !== e.$thumbs) {
                    var t = void 0 !== e.thumbsIsVertical && e.thumbsIsVertical;
                    (e.thumbsIsVertical = e._isPgvertical && window.innerWidth >= Riode.minDesktopWidth),
                        e.thumbsIsVertical
                            ? (e.$thumbs.hasClass("owl-carousel") && e.$thumbs.trigger("destroy.owl.carousel").removeClass("owl-carousel"),
                              (e.thumbsHeight = e.$productThumb[0].offsetHeight * e.thumbsCount + parseInt(e.$productThumb.css("margin-bottom")) * (e.thumbsCount - 1)),
                              e.$thumbUp.addClass("disabled"),
                              e.$thumbDown.toggleClass("disabled", e.thumbsHeight <= e.$thumbsWrap[0].offsetHeight),
                              e.isQuickview && n())
                            : (t && e.$thumbs.css("top", ""),
                              e.$thumbs.hasClass("owl-carousel") || e.$thumbs.addClass("owl-carousel").owlCarousel($.extend(!0, e.isQuickview ? { onInitialized: n, onResized: n } : {}, Riode.defaults.sliderThumbs)));
                }
            },
            n = function () {
                this.$wrapper.find(".product-details").css("height", window.innerWidth > 767 ? this.$wrapper.find(".product-gallery")[0].clientHeight : "");
            };
        return (
            (e.prototype.init = function (e) {
                var a = this,
                    s = e.find(".product-single-carousel");
                (a.$wrapper = e),
                    (a.isQuickview = !!e.closest(".mfp-content").length),
                    (a._isPgvertical = !1),
                    a.isQuickview && ((n = n.bind(this)), Riode.ratingTooltip()),
                    s
                        .on("initialized.owl.carousel", function (e) {
                            a.isQuickview || s.append('<a href="#" class="product-image-full"></a>'),
                                (function (e) {
                                    (e.$thumbs = e.$wrapper.find(".product-thumbs")),
                                        (e.$thumbsWrap = e.$thumbs.parent()),
                                        (e.$thumbUp = e.$thumbsWrap.find(".thumb-up")),
                                        (e.$thumbDown = e.$thumbsWrap.find(".thumb-down")),
                                        (e.$thumbsDots = e.$thumbs.children()),
                                        (e.thumbsCount = e.$thumbsDots.length),
                                        (e.$productThumb = e.$thumbsDots.eq(0)),
                                        (e._isPgvertical = e.$thumbsWrap.parent().hasClass("wrap-slick3")),
                                        (e.thumbsIsVertical = e._isPgvertical && window.innerWidth >= Riode.minDesktopWidth),
                                        e.$thumbDown.on("click", function (i) {
                                            e.thumbsIsVertical && t(e);
                                        }),
                                        e.$thumbUp.on("click", function (t) {
                                            e.thumbsIsVertical && i(e);
                                        }),
                                        e.$thumbsDots.on("click", function () {
                                            var t = $(this),
                                                i = (t.parent().filter(e.$thumbs).length ? t : t.parent()).index();
                                            e.$wrapper.find(".product-single-carousel").trigger("to.owl.carousel", i);
                                        }),
                                        o(e),
                                        Riode.$window.on("resize", function () {
                                            o(e);
                                        });
                                })(a);
                        })
                        .on("translate.owl.carousel", function (e) {
                            var t = (e.item.index - $(e.currentTarget).find(".cloned").length / 2 + e.item.count) % e.item.count;
                            a.thumbsSetActive(t);
                        }),
                    "complete" === Riode.status && (Riode.slider(s), Riode.quantityInput(e.find(".quantity")));
            }),
            (e.prototype.thumbsSetActive = function (e) {
                var t = this.$thumbsDots.eq(e);
                if ((this.$thumbsDots.filter(".active").removeClass("active"), t.addClass("active"), this.thumbsIsVertical)) {
                    var i = parseInt(this.$thumbs.css("top")) + e * this.thumbsHeight;
                    i < 0
                        ? this.$thumbs.css("top", parseInt(this.$thumbs.css("top")) - i)
                        : (i = this.$thumbs.offset().top + this.$thumbs[0].offsetHeight - t.offset().top - t[0].offsetHeight) < 0 && this.$thumbs.css("top", parseInt(this.$thumbs.css("top")) + i);
                } else this.$thumbs.trigger("to.owl.carousel", e, 100);
            }),
            (e.prototype.variationCheck = function () {
                var e = !0;
                this.$selects.each(function () {
                    return this.value || (e = !1);
                }),
                    this.$items.each(function () {
                        var t = $(this);
                        if (t.children("a:not(.size-guide)").length) return t.children(".active").length || (e = !1);
                    }),
                    e ? this.variationMatch() : this.variationClean();
            }),
            (e.prototype.variationMatch = function () {
                this.$priceWrap.find("span").text("$" + (Math.round(50 * Math.random()) + 200) + ".00"), this.$priceWrap.slideDown(), this.$clean.slideDown(), this.$btnCart.removeAttr("disabled");
            }),
            (e.prototype.variationClean = function (e) {
                e && this.$selects.val(""), e && this.$items.children(".active").removeClass("active"), this.$priceWrap.slideUp(), this.$clean.css("display", "none"), this.$btnCart.attr("disabled", "disabled");
            }),
            function (t, i) {
                return t ? new e(t.eq(0), i) : null;
            }
        );
    })()),
    (Riode.initProductSinglePage = (function () {
        function e(e) {
            var t = $(e.currentTarget).closest(".product-single");
            $(".cart-added-alert").remove(),
                $(Riode.parseTemplate(Riode.defaults.templateCartAddedAlert, { name: t.find("h1.product-name").text() }))
                    .insertBefore(t)
                    .fadeIn(),
                $(".sticky-sidebar").trigger("recalc.pin");
        }
        function t(e) {
            e.preventDefault();
            var t,
                i = $(e.currentTarget).closest(".product-single");
            if (
                (t = i.find(".product-single-carousel").length
                    ? i.find(".product-single-carousel .owl-item:not(.cloned) img")
                    : i.find(".product-gallery-carousel").length
                    ? i.find(".product-gallery-carousel .owl-item:not(.cloned) img")
                    : i.find(".product-gallery img")).length
            ) {
                var o = t
                        .map(function () {
                            var e = $(this);
                            return { src: e.attr("data-zoom-image"), w: 800, h: 899, title: e.attr("alt") };
                        })
                        .get(),
                    n = i.find(".product-single-carousel, .product-gallery-carousel").data("owl.carousel"),
                    a = n ? (n.current() - n.clones().length / 2 + o.length) % o.length : i.find(".product-gallery > *").index();
                if ("undefined" != typeof PhotoSwipe) {
                    var s = $(".pswp")[0],
                        d = new PhotoSwipe(s, PhotoSwipeUI_Default, o, { index: a, closeOnScroll: !1 });
                    d.init(), (Riode.photoswipe = d);
                }
            }
        }
        function i(e) {
            var t = $(e.currentTarget);
            t.hasClass("added") ||
                (e.preventDefault(),
                t.addClass("load-more-overlay loading"),
                setTimeout(function () {
                    t.removeClass("load-more-overlay loading").html('<i class="d-icon-heart-full"></i> Browse wishlist').addClass("added").attr("title", "Browse wishlist").attr("href", "wishlist.html");
                }, 500));
        }
        return function () {
            var o = $(".product-single");
            return (
                Riode.$body.on("click", ".product-single .btn-wishlist", i),
                o.length
                    ? document.body.classList.contains("home")
                        ? (o.each(function () {
                              Riode.initProductSingle($(this));
                          }),
                          null)
                        : null === Riode.initProductSingle(o)
                        ? null
                        
                    : null
            );
        };
    })()),
    (Riode.slider = (function () {
        function e(e, t) {
            return this.init(e, t);
        }
        var t = function (e) {
                var t,
                    i = ["", "-xs", "-sm", "-md", "-lg", "-xl"];
                for (this.classList.remove("row"), a = 0; a < 6; ++a) for (t = 1; t <= 12; ++t) this.classList.remove("cols" + i[a] + "-" + t);
                if ((this.classList.remove("gutter-no"), this.classList.remove("gutter-sm"), this.classList.remove("gutter-lg"), this.classList.contains("animation-slider")))
                    for (var o = this.children, n = o.length, a = 0; a < n; ++a) o[a].setAttribute("data-index", a + 1);
            },
            i = function (e) {
                var t,
                    i = this.firstElementChild.firstElementChild.children,
                    o = i.length;
                for (t = 0; t < o; ++t)
                    if (!i[t].classList.contains("active")) {
                        var n,
                            a = Riode.byClass("appear-animate", i[t]);
                        for (n = a.length - 1; n >= 0; --n) a[n].classList.remove("appear-animate");
                    }
                var s = $(e.currentTarget);
                s.find("video").on("ended", function () {
                    $(this).closest(".owl-item").hasClass("active") &&
                        (!0 === s.data("owl.carousel").options.autoplay
                            ? (!1 === s.data("owl.carousel").options.loop && s.data().children - 1 === s.find(".owl-item.active").index() && ((this.loop = !0), this.play()), s.trigger("next.owl.carousel"), s.trigger("play.owl.autoplay"))
                            : ((this.loop = !0), this.play()));
                });
            },
            o = function (e) {
                $(window).trigger("appear.check");
                var t = $(e.currentTarget),
                    i = t.find(".owl-item.active video");
                t.find(".owl-item:not(.active) video").each(function () {
                    this.paused || t.trigger("play.owl.autoplay"), this.pause(), (this.currentTime = 0);
                }),
                    i.length &&
                        (!0 === t.data("owl.carousel").options.autoplay && t.trigger("stop.owl.autoplay"),
                        i.each(function () {
                            this.paused && this.play();
                        }));
            },
            n = function (e) {
                var t = this;
                $(e.currentTarget)
                    .find(".owl-item.active .slide-animate")
                    .each(function () {
                        var e = $(this),
                            i = $.extend(!0, {}, Riode.defaults.animation, Riode.parseOptions(e.data("animation-options"))),
                            o = i.duration,
                            n = i.delay,
                            a = i.name;
                        e.css("animation-duration", o);
                        var s = Riode.requestTimeout(
                            function () {
                                e.addClass(a), e.addClass("show-content");
                            },
                            n ? 1e3 * Number(n.slice(0, -1)) : 0
                        );
                        t.timers.push(s);
                    });
            },
            a = function (e) {
                $(e.currentTarget)
                    .find(".owl-item.active .slide-animate")
                    .each(function () {
                        var e = $(this);
                        e.addClass("show-content"), e.attr("style", "");
                    });
            },
            s = function (e) {
                var t = $(e.currentTarget);
                (this.translateFlag = 1),
                    (this.prev = this.next),
                    t.find(".owl-item .slide-animate").each(function () {
                        var e = $(this),
                            t = $.extend(!0, {}, Riode.defaults.animation, Riode.parseOptions(e.data("animation-options")));
                        e.removeClass(t.name);
                    });
            },
            d = function (e) {
                var t = this,
                    i = $(e.currentTarget);
                if (1 == t.translateFlag) {
                    if (((t.next = i.find(".owl-item").eq(e.item.index).children().attr("data-index")), i.find(".show-content").removeClass("show-content"), t.prev != t.next)) {
                        if ((i.find(".show-content").removeClass("show-content"), i.hasClass("animation-slider"))) {
                            for (var o = 0; o < t.timers.length; o++) Riode.deleteTimeout(t.timers[o]);
                            t.timers = [];
                        }
                        i.find(".owl-item.active .slide-animate").each(function () {
                            var e = $(this),
                                i = $.extend(!0, {}, Riode.defaults.animation, Riode.parseOptions(e.data("animation-options"))),
                                o = i.duration,
                                n = i.delay,
                                a = i.name;
                            e.css("animation-duration", o),
                                e.css("animation-delay", n),
                                e.css("transition-property", "visibility, opacity"),
                                e.css("transition-delay", n),
                                e.css("transition-duration", o),
                                e.addClass(a),
                                (o = o || "0.75s"),
                                e.addClass("show-content");
                            var s = Riode.requestTimeout(
                                function () {
                                    e.css("transition-property", ""), e.css("transition-delay", ""), e.css("transition-duration", ""), t.timers.splice(t.timers.indexOf(s), 1);
                                },
                                n ? 1e3 * Number(n.slice(0, -1)) + 500 * Number(o.slice(0, -1)) : 500 * Number(o.slice(0, -1))
                            );
                            t.timers.push(s);
                        });
                    } else i.find(".owl-item").eq(e.item.index).find(".slide-animate").addClass("show-content");
                    t.translateFlag = 0;
                }
            };
        return (
            (e.zoomImage = function () {
                Riode.zoomImage(this.$element);
            }),
            (e.zoomImageRefresh = function () {
                this.$element.find("img").each(function () {
                    var e = $(this);
                    if ($.fn.elevateZoom) {
                        var t = e.data("elevateZoom");
                        void 0 !== t ? t.refresh() : ((Riode.defaults.zoomImage.zoomContainer = e.parent()), e.elevateZoom(Riode.defaults.zoomImage));
                    }
                });
            }),
            (Riode.defaults.sliderPresets["product-single-carousel"].onInitialized = Riode.defaults.sliderPresets["product-gallery-carousel"].onInitialized = e.zoomImage),
            (Riode.defaults.sliderPresets["product-single-carousel"].onRefreshed = Riode.defaults.sliderPresets["product-gallery-carousel"].onRefreshed = e.zoomImageRefresh),
            (e.prototype.init = function (e, r) {
                (this.timers = []), (this.translateFlag = 0), (this.prev = 1), (this.next = 1), Riode.lazyload(e, !0);
                var l = e.attr("class").split(" "),
                    c = $.extend(!0, {}, Riode.defaults.slider);
                l.forEach(function (e) {
                    var t = Riode.defaults.sliderPresets[e];
                    t && $.extend(!0, c, t);
                });
                e.find("video").each(function () {
                    this.loop = !1;
                }),
                    $.extend(!0, c, Riode.parseOptions(e.attr("data-owl-options")), r),
                    (n = n.bind(this)),
                    (s = s.bind(this)),
                    (d = d.bind(this)),
                    e.on("initialize.owl.carousel", t).on("initialized.owl.carousel", i).on("translated.owl.carousel", o),
                    e.hasClass("animation-slider") && e.on("initialized.owl.carousel", n).on("resized.owl.carousel", a).on("translate.owl.carousel", s).on("translated.owl.carousel", d),
                    e.owlCarousel(c);
            }),
            function (t, i) {
                Riode.$(t).each(function () {
                    var t = $(this);
                    Riode.call(function () {
                        new e(t, i);
                    });
                });
            }
        );
    })()),

    (Riode.Menu = {
        init: function () {
            this.initMenu(), this.initMobileMenu(), this.initFilterMenu(), this.initCategoryMenu(), this.initCollapsibleWidget();
        },
        initMenu: function () {
            // $(".menu li").each(function () {
            //     this.lastElementChild && ("UL" === this.lastElementChild.tagName || this.lastElementChild.classList.contains("megamenu")) && this.classList.add("submenu");
            // }),
            //     $(".main-nav .megamenu, .main-nav .submenu > ul").each(function () {
            //         var e = $(this),
            //             t = e.offset().left,
            //             i = t + e.outerWidth() - (window.innerWidth - 20);
            //         i >= 0 && t > 20 && e.css("margin-left", "-=" + i);
            //     }),
            //     Riode.$window.on("resize", function () {
            //         $(".main-nav .megamenu, .main-nav .submenu > ul").each(function () {
            //             var e = $(this),
            //                 t = e.offset().left,
            //                 i = t + e.outerWidth() ;
            //             i >= 0 && t > 20 && e.css("margin-left", "-=" + i);
            //         });
            //     });

        },
        initMobileMenu: function () {
            function e() {
                Riode.$body.removeClass("mmenu-active");
            }
            $(".mobile-menu li, .toggle-menu li").each(function () {
                if (this.lastElementChild && ("UL" === this.lastElementChild.tagName || this.lastElementChild.classList.contains("megamenu"))) {
                    var e = document.createElement("span");
                    (e.className = "toggle-btn"), this.firstElementChild.appendChild(e);
                }
            }),
                $(".mobile-menu-toggle").on("click", function () {
                    Riode.$body.addClass("mmenu-active");
                }),
                $(".mobile-menu-overlay").on("click", e),
                $(".mobile-menu-close").on("click", e),
                Riode.$window.on("resize", e);
        },
        initFilterMenu: function () {
            $(".search-ul li").each(function () {
                if (this.lastElementChild && "UL" === this.lastElementChild.tagName) {
                    var e = document.createElement("i");
                    (e.className = "fas fa-chevron-down"), this.classList.add("with-ul"), this.firstElementChild.appendChild(e);
                }
            }),
                 
        },
        initCategoryMenu: function () {
            var e = $(".category-dropdown");
            if (e.length) {
                var t = e.find(".dropdown-box");
                if (t.length) {
                    var i = $(".main").offset().top + t[0].offsetHeight;
                    (window.pageYOffset > i || window.innerWidth < Riode.minDesktopWidth) && e.removeClass("show"),
                        window.addEventListener(
                            "scroll",
                            function () {
                                window.pageYOffset <= i && window.innerWidth >= Riode.minDesktopWidth && e.removeClass("show");
                            },
                            { passive: !0 }
                        ),
                        $(".category-toggle").on("click", function (e) {
                            e.preventDefault();
                        }),
                        e.on("mouseover", function (t) {
                            window.pageYOffset > i && window.innerWidth >= Riode.minDesktopWidth && e.addClass("show");
                        }),
                        e.on("mouseleave", function (t) {
                            window.pageYOffset > i && window.innerWidth >= Riode.minDesktopWidth && e.removeClass("show");
                        });
                }
                if (e.hasClass("with-sidebar")) {
                    var o = Riode.byClass("sidebar");
                    o.length &&
                        (e.find(".dropdown-box").css("width", o[0].offsetWidth - 20),
                        Riode.$window.on("resize", function () {
                            e.find(".dropdown-box").css("width", o[0].offsetWidth - 20);
                        }));
                }
            }
        },
        initCollapsibleWidget: function () {
            $(".widget-collapsible .widget-title").each(function () {
                var e = document.createElement("span");
                (e.className = "toggle-btn"), this.appendChild(e);
            }),
                $(".widget-collapsible .widget-title").on("click", function (e) {
                    var t = $(this);
                    if (!t.hasClass("sliding")) {
                        var i = t.siblings(".widget-body");
                        t.hasClass("collapsed") || i.css("display", "block"),
                            t.addClass("sliding"),
                            i.slideToggle(300, function () {
                                t.removeClass("sliding");
                            }),
                            t.toggleClass("collapsed"),
                            setTimeout(function () {
                                $(".sticky-sidebar").trigger("recalc.pin");
                            }, 320);
                    }
                });
        },
    }),
    (Riode.Minipopup = (function () {
        var e,
            t = 0,
            i = [],
            o = !1,
            n = [],
            a = !1,
            s = function () {
                if (!o) for (var e = 0; e < n.length; ++e) (n[e] -= 200) <= 0 && this.close(e--);
            };
        return {
            init: function () {
                var t = document.createElement("div");
                (t.className = "minipopup-area"),
                    Riode.byClass("page-wrapper")[0].appendChild(t),
                    (e = $(t)).on("click", ".btn-close", function (e) {
                        self.close($(this).closest(".minipopup-box").index());
                    }),
                    (this.close = this.close.bind(this)),
                    (s = s.bind(this));
            },
            open: function (o, d) {
                var r,
                    l = this,
                    c = $.extend(!0, {}, Riode.defaults.minipopup, o);
                c.isPurchased ? (c.detailTemplate = Riode.parseTemplate(c.purchasedTemplate, c)) : (c.detailTemplate = Riode.parseTemplate(null != c.count ? c.priceQuantityTemplate : c.priceTemplate, c)),
                    null != c.rating && (c.detailTemplate += Riode.parseTemplate(c.ratingTemplate, c)),
                    (r = $(Riode.parseTemplate(c.template, c))),
                    (l.space = c.space),
                    (r.appendTo(e).css("top", -t).find("img")[0].onload = function () {
                        (t += r[0].offsetHeight + l.space),
                            r.addClass("show"),
                            r.offset().top - window.pageYOffset < 0 && (l.close(), r.css("top", -t + r[0].offsetHeight + l.space)),
                            r
                                .on("mouseenter", function () {
                                    l.pause();
                                })
                                .on("mouseleave", function () {
                                    l.resume();
                                })
                                .on("touchstart", function (e) {
                                    l.pause(), e.stopPropagation();
                                })
                                .on("mousedown", function () {
                                    $(this).addClass("focus");
                                })
                                .on("mouseup", function () {
                                    l.close($(this).index());
                                }),
                            Riode.$body.on("touchstart", function () {
                                l.resume();
                            }),
                            i.push(r),
                            n.push(c.delay),
                            n.length > 1 || (a = setInterval(s, 200)),
                            d && d(r);
                    });
            },
            close: function (e) {
                var o = void 0 === e ? 0 : e,
                    s = i.splice(o, 1)[0];
                n.splice(o, 1)[0],
                    (t -= s[0].offsetHeight + this.space),
                    s.removeClass("show"),
                    setTimeout(function () {
                        s.remove();
                    }, 300),
                    i.forEach(function (e, t) {
                        t >= o && e.hasClass("show") && e.stop(!0, !0).animate({ top: parseInt(e.css("top")) + e[0].offsetHeight + 20 }, 600, "easeOutQuint");
                    }),
                    i.length || clearTimeout(a);
            },
            pause: function () {
                o = !0;
            },
            resume: function () {
                o = !1;
            },
        };
    })()),
    (Riode.floatSVG = (function () {
        function e(e, t) {
            (this.$el = $(e)), this.set(t), this.start();
        }
        return (
            (e.prototype.set = function (e) {
                this.options = $.extend({ delta: 15, speed: 10, size: 1 }, "string" == typeof e ? Riode.parseOptions(e) : e);
            }),
            (e.prototype.getDeltaY = function (e) {
                return Math.sin(((2 * Math.PI * e) / this.width) * this.options.size) * this.options.delta;
            }),
            (e.prototype.start = function () {
                (this.update = this.update.bind(this)),
                    (this.timeStart = Date.now() - parseInt(100 * Math.random())),
                    this.$el.find("path").each(function () {
                        $(this).data("original", this.getAttribute("d").replace(/([\d])\s*\-/g, "$1,-"));
                    }),
                    window.addEventListener("resize", this.update, { passive: !0 }),
                    window.addEventListener("scroll", this.update, { passive: !0 }),
                    Riode.$window.on("check_float_svg", this.update),
                    this.update();
            }),
            (e.prototype.update = function () {
                var e = this;
                this.$el.length &&
                    Riode.isOnScreen(this.$el[0]) &&
                    Riode.requestTimeout(function () {
                        e.draw();
                    }, 16);
            }),
            (e.prototype.draw = function () {
                var e = this,
                    t = ((Date.now() - this.timeStart) * this.options.speed) / 200;
                (this.width = this.$el.width()),
                    this.width &&
                        (this.$el.find("path").each(function () {
                            var i = t,
                                o = 0;
                            this.setAttribute(
                                "d",
                                $(this)
                                    .data("original")
                                    .replace(/M([\d|\.]*),([\d|\.]*)/, function (t, n, a) {
                                        return n && a ? "M" + n + "," + (parseFloat(a) + (o = e.getDeltaY((i += parseFloat(n))))).toFixed(3) : t;
                                    })
                                    .replace(/([c|C])[^A-Za-z]*/g, function (n, a) {
                                        if (a) {
                                            var s = n.slice(1).split(",").map(parseFloat);
                                            if (6 == s.length)
                                                return (
                                                    "C" == a
                                                        ? ((s[1] += e.getDeltaY(t + s[0])), (s[3] += e.getDeltaY(t + s[2])), (s[5] += e.getDeltaY((i = t + s[4]))))
                                                        : ((s[1] += e.getDeltaY(i + s[0]) - o), (s[3] += e.getDeltaY(i + s[2]) - o), (s[5] += e.getDeltaY((i += s[4])) - o)),
                                                    (o = e.getDeltaY(i)),
                                                    a +
                                                        s
                                                            .map(function (e) {
                                                                return e.toFixed(3);
                                                            })
                                                            .join(",")
                                                );
                                        }
                                        return n;
                                    })
                            );
                        }),
                        this.update());
            }),
            function (t) {
                Riode.$(t).each(function () {
                    var t,
                        i = $(this);
                    "svg" == this.tagName && ((t = i.data("float-svg")) ? t.set(i.attr("data-float-options")) : i.data("float-svg", new e(this, i.attr("data-float-options"))));
                });
            }
        );
    })()),
    (Riode.Shop = {
        init: function () {
            // this.initProductsQuickview(),
                this.initProductsCartAction(),
                this.initProductsLoad(),
                this.initProductsScrollLoad(".scroll-load"),
                this.initProductType("slideup"),
                this.initVariation(),
                this.initWishlistButton(".product:not(.product-single) .btn-wishlist"),
                Riode.call(Riode.ratingTooltip, 500),
                this.initSelectMenu(".select-menu"),
                Riode.priceSlider(".filter-price-slider");
        },
        initVariation: function (e) {
            $(".product:not(.product-single) .product-variations > a").on("click", function (e) {
                var t = $(this),
                    i = t.closest(".product").find(".product-media img");
                i.data("image-src") || i.data("image-src", i.attr("src")),
                    t.toggleClass("active").siblings().removeClass("active"),
                    t.hasClass("active") ? i.attr("src", t.data("src")) : (i.attr("src", i.data("image-src")), t.blur()),
                    e.preventDefault();
            });
        },
        initProductType: function (e) {
            "slideup" === e &&
                ($(".product-slideup-content .product-details").each(function (e) {
                    var t = $(this),
                        i = t.find(".product-hide-details").outerHeight(!0);
                    t.height(t.height() - i);
                }),
                $(Riode.byClass("product-slideup-content"))
                    .on("mouseenter touchstart", function (e) {
                        var t = $(this),
                            i = t.find(".product-hide-details").outerHeight(!0);
                        t.find(".product-details").css("transform", "translateY(" + -i + "px)"), t.find(".product-hide-details").css("transform", "translateY(" + -i + "px)");
                    })
                    .on("mouseleave touchleave", function (e) {
                        var t = $(this);
                        t.find(".product-hide-details").outerHeight(!0);
                        t.find(".product-details").css("transform", "translateY(0)"), t.find(".product-hide-details").css("transform", "translateY(0)");
                    }));
        },
        initSelectMenu: function () {
            Riode.$body
                .on("mousedown", ".select-menu", function (e) {
                    var t = $(e.currentTarget),
                        i = $(e.target),
                        o = t.hasClass("opened");
                    t.hasClass("fixed") ? e.stopPropagation() : $(".select-menu").removeClass("opened"),
                        t.is(i.parent())
                            ? (o || t.addClass("opened"), e.stopPropagation())
                            : (i.parent().toggleClass("active"),
                              i.parent().hasClass("active")
                                  ? ($(".select-items").show(),
                                    $('<a href="#" class="select-item">' + i.text() + '<i class="d-icon-times"></i></a>')
                                        .insertBefore(".select-items .filter-clean")
                                        .hide()
                                        .fadeIn()
                                        .data("link", i.parent()))
                                  : $(".select-items > .select-item")
                                        .filter(function (e, t) {
                                            return t.innerText == i.text();
                                        })
                                        .fadeOut(function () {
                                            $(this).remove(), $(".select-items").children().length < 2 && $(".select-items").hide();
                                        }));
                })
                .on("mousedown", function (e) {
                    $(".select-menu").removeClass("opened");
                })
                .on("click", ".select-menu a", function (e) {
                    e.preventDefault();
                })
                .on("click", ".select-items .filter-clean", function (e) {
                    var t = $(this);
                    t.siblings().each(function () {
                        var e = $(this).data("link");
                        e && e.removeClass("active");
                    }),
                        t.parent().fadeOut(function () {
                            t.siblings().remove();
                        }),
                        e.preventDefault();
                })
                .on("click", ".select-item i", function (e) {
                    $(e.currentTarget)
                        .parent()
                        .fadeOut(function () {
                            var e = $(this),
                                t = e.data("link");
                            t && t.toggleClass("active"), e.remove(), $(".select-items").children().length < 2 && $(".select-items").hide();
                        }),
                        e.preventDefault();
                })
                .on("click", ".filter-clean", function (e) {
                    $(".shop-sidebar .filter-items .active").removeClass("active"), e.preventDefault();
                })
                .on("click", ".filter-items a", function (e) {
                    var t = $(this).closest(".filter-items");
                    t.hasClass("search-ul") ||
                        t.parent().hasClass("select-menu") ||
                        (t.hasClass("filter-price") ? ($(this).parent().siblings().removeClass("active"), $(this).parent().toggleClass("active"), e.preventDefault()) : ($(this).parent().toggleClass("active"), e.preventDefault()));
                });
        },
        // initProductsQuickview: function () {
        //     Riode.$body.on("click", ".btn-quickview", function (e) {
        //         e.preventDefault(),
        //             Riode.popup(
        //                 {
        //                     items: { src: "ajax/quickview.html" },
        //                     callbacks: {
        //                         ajaxContentAdded: function () {
        //                             this.wrap.imagesLoaded(function () {
        //                                 Riode.initProductSingle($(".mfp-product .product-single"));
        //                             });
        //                         },
        //                     },
        //                 },
        //                 "quickview"
        //             );
        //     });
        // },
        initProductsCartAction: function () {
            Riode.$body
                .on("click", ".cart-offcanvas .cart-toggle", function (e) {
                    $(".cart-dropdown").addClass("opened"), e.preventDefault();
                })
                .on("click", ".cart-offcanvas .cart-header .btn-close", function (e) {
                    $(".cart-dropdown").removeClass("opened"), e.preventDefault();
                })
                .on("click", ".cart-offcanvas .cart-overlay", function (e) {
                    $(".cart-dropdown").removeClass("opened"), e.preventDefault();
                })
                // .on("click", ".product:not(.product-variable) .btn-product-icon.btn-cart, .product:not(.product-variable) .btn-product.btn-cart", function (e) {
                //     e.preventDefault();
                //     var t = $(this).closest(".product");
                //     t.hasClass("product-single") ||
                //         Riode.Minipopup.open({
                //             message: "Successfully Added",
                //             productClass: " product-cart",
                //             name: t.find(".product-name").text(),
                //             nameLink: t.find(".product-name > a").attr("href"),
                //             imageSrc: t.find(".product-media img").attr("src"),
                //             imageLink: t.find(".product-name > a").attr("href"),
                //             price: t.find(".product-price .new-price, .product-price .price").html(),
                //             count: t.find(".quantity").length > 0 ? t.find(".quantity").val() : 1,
                //             actionTemplate:
                //                 `<div class="action-group d-flex"><a href="/panier" class="btn btn-sm btn-outline btn-primary btn-rounded">Voir Panier</a></div>`
                //         });
                // });
        },
        initProductsLoad: function () {
            $(".btn-load").on("click", function (e) {
                var t = $(this),
                    i = $(t.data("load-to")),
                    o = t.html();
                t.text("Loading ..."),
                    t.addClass("btn-loading"),
                    $(".d-loading").css("display", "block"),
                    e.preventDefault(),
                    $.ajax({
                        url: t.attr("href"),
                        success: function (e) {
                            var n = $(e);
                            setTimeout(function () {
                                i.isotope("insert", n), t.html(o);
                                var e = parseInt(t.data("load-count") ? t.data("load-count") : 0);
                                t.data("load-count", ++e), t.removeClass("btn-loading"), $(".d-loading").css("display", "none"), e >= 2 && t.hide();
                            }, 350);
                        },
                        failure: function () {
                            t.text("Sorry something went wrong.");
                        },
                    });
            });
        },

        initProductsScrollLoad: function (e) {
            var t,
                i = Riode.$(e),
                o = $(e).data("url");
            o || (o = "ajax/ajax-products.html");
            var n = function (e) {
                window.pageYOffset > t + i.outerHeight() - window.innerHeight - 150 &&
                    "loading" != i.data("load-state") &&
                    $.ajax({
                        url: o,
                        success: function (e) {
                            var t = $(e);
                            i.data("load-state", "loading"),
                                i.next().hasClass("load-more-overlay") ? i.next().addClass("loading") : $('<div class="mt-4 mb-4 load-more-overlay loading"></div>').insertAfter(i),
                                setTimeout(function () {
                                    i.next().removeClass("loading"),
                                        i.append(t),
                                        setTimeout(function () {
                                            i.find(".product-wrap.fade:not(.in)").addClass("in");
                                        }, 200),
                                        i.data("load-state", "loaded");
                                }, 500);
                            var o = parseInt(i.data("load-count") ? i.data("load-count") : 0);
                            i.data("load-count", ++o), o > 2 && window.removeEventListener("scroll", n, { passive: !0 });
                        },
                        failure: function () {
                            $this.text("Sorry something went wrong.");
                        },
                    });
            };
            i.length > 0 && ((t = i.offset().top), window.addEventListener("scroll", n, { passive: !0 }));
        },
        initWishlistButton: function (e) {
            Riode.$body.on("click", e, function (e) {
                var t = $(this);
                t.toggleClass("added").addClass("load-more-overlay loading"),
                    setTimeout(function () {
                        t.removeClass("load-more-overlay loading").find("i").toggleClass("d-icon-heart").toggleClass("d-icon-heart-full"), t.hasClass("added") ? t.attr("title", "Remove from wishlist") : t.attr("title", "Add to wishlist");
                    }, 500),
                    e.preventDefault();
            });
        },
    }),
    (Riode.prepare = function () {
        Riode.$body.hasClass("with-flex-container") && window.innerWidth >= 1200 && Riode.$body.addClass("sidebar-active");
    }),
    // HNNNNNNNNNNNNNNNNNNNNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    // (Riode.uncheckSibligs = function () {
    //     $(".sidebar-content input:checkbox").on('click', function() {
    //         console.log("this was clicked");
    //         // in the handler, 'this' refers to the box clicked on
    //         var $box = $(this);
    //         if ($box.is(":checked")) {
    //         // the name of the box is retrieved using the .attr() method
    //         // as it is assumed and expected to be immutable
    //         var group = "input:checkbox[name='" + $box.attr("name") + "']";
    //         // the checked state of the group/box on the other hand will change
    //         // and the current value is retrieved using .prop() method
    //         $(group).prop("checked", false);
    //         $box.prop("checked", true);
    //         } else {
    //         $box.prop("checked", false);
    //         }
    //     });
    // }),
    
    (Riode.initLayout = function () {
        Riode.isotopes(".grid:not(.grid-float)"), Riode.stickySidebar(".sticky-sidebar");
    }),
    (Riode.init = function () {
        Riode.appearAnimate(".appear-animate"),
            Riode.Minipopup.init(),
            Riode.Shop.init(),
            Riode.initProductSinglePage(),
            Riode.slider(".owl-carousel"),
            Riode.headerToggleSearch(".hs-toggle"),
            Riode.closeTopNotice(".btn-notice-close"),
            Riode.stickyContent(".product-sticky-content, .sticky-header", { top: !1 }),
            Riode.stickyContent(".sticky-footer", Riode.defaults.stickyFooter),
            Riode.stickyContent(".sticky-toolbox", Riode.defaults.stickyToolbox),
            Riode.sidebar("sidebar"),
            Riode.sidebar("right-sidebar"),
            Riode.sidebar("top-sidebar"),
            // Riode.quantityInput(".quantity"),
            Riode.playableVideo(".post-video"),
            Riode.initAccordion(".card-header > a"),
            Riode.initTab(".nav-tabs"),
            Riode.initAlert(".alert"),
            Riode.parallax(".parallax"),
            Riode.countTo(".count-to"),
            Riode.countdown(".product-countdown, .countdown"),
            Riode.Menu.init(),
            Riode.initZoom(),
            // Riode.uncheckSibligs(),
            Riode.initNavFilter(".nav-filters .nav-filter"),
            //Riode.initPopups(),
            //Riode.initPurchasedMinipopup(),
            
            Riode.initScrollTopButton(),
            Riode.floatSVG(".float-svg"),
            Riode.initShowVendorSearch(".toolbox .form-toggle-btn"),
            (Riode.status = "complete");
    }),
    Riode.prepare(),
    (window.onload = function () {
        (Riode.status = "loaded"), Riode.$body.addClass("loaded"), Riode.$window.trigger("riode_load"), Riode.call(Riode.initLayout), Riode.call(Riode.init), Riode.$window.trigger("riode_complete"), Riode.refreshSidebar();
    });


    document.addEventListener("DOMContentLoaded", function() {
        // Get all elements with the class "btntn" and convert them to an array
        var buttons = Array.from(document.getElementsByClassName("toggle-btn"));
      
        // Use forEach to attach a click event listener to each button
        buttons.forEach(function(button) {
          button.addEventListener("click", function(e) {
            // Print "hello" to the console
            console.log("hello");
            $(this).parent().next().slideToggle(300).parent().toggleClass("show"),
			setTimeout(function () {
				$(".sticky-sidebar").trigger("recalc.pin");
			}, 320),
			e.preventDefault();
          });
        });

        
        

        
      });


      
     


     
     
 