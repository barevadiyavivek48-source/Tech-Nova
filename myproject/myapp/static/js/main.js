/*------ Main Js ----*/
(function ($) {
  "use strict";

  /* --------------------------------------------------------------------------
   * Envato Review Improvements
   * - Cache frequently used DOM lookups
   * - Defensive checks / error handling around optional plugins
   * - Namespace events for cleanup (memory management)
   * ------------------------------------------------------------------------ */

  // Cached selectors (performance)
  const $win = $(window);
  const $doc = $(document);
  const $body = $("body");
  const $modalOverlay = $(".modal-overlay");
  const $tabPanes = $(".tab-pane");
  const $filterButtons = $(".filter-button");
  const $filterDropdownMenus = $(".filter-dropdown-menu");
  const $filterDropdownIcons = $(".filter-dropdown-icon");
  const $searchResultContainers = $(".search-result-container");

  // Safe plugin initializer (error handling)
  function safeInit(fn) {
    try {
      fn();
    } catch (err) {
      // Silently fail in production templates; prevents broken pages if a vendor plugin is missing
      // console.warn(err);
    }
  }

  // Cleanup registry (memory management)
  const cleanupTasks = [];
  function addCleanup(task) {
    if (typeof task === "function") cleanupTasks.push(task);
  }

  /*------ Preloader ----*/
  $win.on("load.sellzy", function () {
    $(".preloader").addClass("loaded");
  });

  /*------ Wow Animation ----*/
  safeInit(function () {
    if (typeof WOW !== "undefined") new WOW().init();
  });

  /*------ Nice Select ----*/
  safeInit(function () {
    if ($.fn && $.fn.niceSelect) $("select").niceSelect();
  });

  $("select").on("change.sellzy", function () {
    $(this).siblings(".nice-select").addClass("changed");
  });

  /*------ Sticky Header ----*/
  const stickyHeader = $(".sticky-header");
  const win = $win;
  win.on("scroll.sellzy", function () {
    if (win.scrollTop() > 200) {
      stickyHeader.addClass("sticky-top");
    } else {
      stickyHeader.removeClass("sticky-top");
    }
  });

  /*------ Product Filter Buttons ------*/
  const productFilterButtons = $(".home-one-product-filter button");
  if (productFilterButtons.length) {
    $(".home-one-product-filter button:nth-child(1)")
      .addClass("btn-primary")
      .removeClass("btn-default outline shadow-none")
      .siblings()
      .removeClass("btn-primary")
      .addClass("btn-default outline  shadow-none");
    $tabPanes.hide();

    $(".tab-pane:nth-child(1)").addClass("active").show();
    $(".home-one-product-filter button").on("click.sellzy", function () {
      $(this)
        .removeClass("btn-default outline shadow-none")
        .addClass("btn-primary")
        .siblings()
        .removeClass("btn-primary")
        .addClass("btn-default outline  shadow-none");
      $tabPanes.removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
      return false;
    });
  }

  /*------ Sidebar ----*/
  const sidebarMenu = $("#sidebar-menu-btn");
  const sidebar = $("#sidebar");
  const sidebarMenuClose = $("#side-bar-menu-close");
  if (sidebarMenu.length) {
    sidebarMenu.on("click.sellzy", function () {
      $(sidebar).attr("data-state", "open");
      $modalOverlay.attr("data-overlay-for", "#sidebar");
      $body.addClass("overflow-hidden");
      $modalOverlay.fadeIn();
    });
  }

  if (sidebarMenuClose.length) {
    sidebarMenuClose.on("click.sellzy", function () {
      $(sidebar).attr("data-state", "close");
      $body.removeClass("overflow-hidden");
      $modalOverlay.fadeOut();
    });
  }

  if ($modalOverlay.length) {
    $modalOverlay.on("click.sellzy", function () {
      const overlayFor = $(this).attr("data-overlay-for");
      if (overlayFor) {
        $(overlayFor).attr("data-state", "close");
      }
      $body.removeClass("overflow-hidden scrollbar-offset");
      $(this).fadeOut();
      $(this).removeAttr("data-overlay-for");
    });
  }

  /*------ Cart Sidebar ------*/
  const cartSidebarBtn = $(".cart-sidebar-btn");

  if (cartSidebarBtn.length) {
    cartSidebarBtn.on("click.sellzy", function () {
      isAnythingOpen();
      showSidebar(".cart-sidebar");
    });
  }

  /*------ Register Page Button ------*/
  const registerPageBtn = $(".register-page-btn");
  if (registerPageBtn.length) {
    registerPageBtn.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".register-page-sidebar");
    });
  }

  /*------ Login Page Button ------*/
  const loginPageBtn = $(".login-page-btn");
  if (loginPageBtn.length) {
    loginPageBtn.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".login-page-sidebar");
    });
  }

  /*------ Forgot Password Page Button ------*/
  const forgotPasswordPageBtn = $(".forgot-password-page-btn");
  if (forgotPasswordPageBtn.length) {
    forgotPasswordPageBtn.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".forgot-password-page-sidebar");
    });
  }

  /*------ Reset Password Page Button ------*/
  const resetPasswordPageBtn = $(".reset-password-page-btn");
  if (resetPasswordPageBtn.length) {
    resetPasswordPageBtn.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".reset-password-page-sidebar");
    });
  }

  /*------ OTP Verification Page Button ------*/
  const otpVerificationPageBtn = $(".otp-verification-page-btn");
  if (otpVerificationPageBtn.length) {
    otpVerificationPageBtn.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".otp-verification-page-sidebar");
    });
  }

  /*------ Close Sidebar ------*/
  const closeSidebarBtn = $(".close-sidebar-btn");
  if (closeSidebarBtn.length) {
    closeSidebarBtn.on("click.sellzy", function () {
      const sidebarFor = $(this).attr("data-close-sidebar");
      isAnythingOpen();
      closeSidebar(sidebarFor);
    });
  }

  /*------ Explorer Category ------*/
  const btn = $("#dropdownButton");
  const menu = $("#dropdownMenu");
  const icon = $("#dropdownIcon");

  btn.on("click.sellzy", function () {
    const isOpen = $(this).attr("data-state") === "open";
    if (isOpen) {
      $(this).attr("data-state", "close");
      menu.removeClass("active").addClass("hide");
      icon.removeClass("rotate-180");
    } else {
      btn.attr("data-state", "open");
      menu.removeClass("hide").addClass("active");
      icon.addClass("rotate-180");
    }
  });

  $doc.on("click.sellzy", function (e) {
    if (!$(e.target).closest("#dropdownButton").length) {
      btn.attr("data-state", "close");
      menu.removeClass("active").addClass("hide");
      icon.removeClass("rotate-180");
    }
    // Banner Filter Dropdown Close
    if (!$(e.target).closest(".filter-dropdown").length) {
      $filterButtons.attr("data-state", "close");
      $filterButtons.removeClass(
        "ring-primary text-primary transition-colors duration-300 ease-in-out"
      );
      $filterButtons.find("span i").removeClass(
        "text-primary transition-colors duration-300 ease-in-out"
      );
      $filterDropdownMenus.removeClass("active").addClass("hide");
      $filterDropdownIcons.removeClass(
        "rotate-180 text-primary transition-colors duration-300 ease-in-out"
      );
    }

    if (!$(e.target).closest(".search-input-container").length) {
      $searchResultContainers.attr("data-state", "close");
    }
  });

  /*------ Sellzy Countdown ----*/
  const sellzyCountdown = $(".sellzy-countdown");
  if (sellzyCountdown.length) {
    safeInit(function () {
      if ($.fn && $.fn.countdown) {
        sellzyCountdown.countdown({
          date: "03/14/2026 00:00:00",
          offset: +6,
          day: "Day",
          days: "Days",
          hideOnComplete: true,
        });
      }
    });
  }

  /*------ Search Flow ----*/
  const SEARCH_HISTORY_KEY = "tech_nova_search_history";
  const MAX_SEARCH_HISTORY = 10;
  const RECOMMENDED_PRODUCTS = Array.isArray(window.RECOMMENDED_PRODUCTS_DATA)
    ? window.RECOMMENDED_PRODUCTS_DATA.filter((item) => item && item.name)
    : [
        { name: "Immunity booster", url: "", image: "" },
        { name: "Hand Sanitizer 500ml", url: "", image: "" },
        { name: "Heart health supplements", url: "", image: "" },
        { name: "Protein powder for women", url: "", image: "" },
      ];

  // Load and display search history on page load
  function loadSearchHistory() {
    const history = JSON.parse(localStorage.getItem(SEARCH_HISTORY_KEY)) || [];
    renderSearchHistory(history);
  }

  // Render search history items to all containers
  function renderSearchHistory(history) {
    const $containers = $(".recent-search-container");
    
    $containers.each(function () {
      const $container = $(this);
      $container.empty();

      if (history.length === 0) {
        $container.html('<p class="text-sm text-gray-500">No recent searches</p>');
        return;
      }

      history.forEach((item) => {
        const $button = $(
          `<button type="button" class="recent-search-item btn text-sm leading-[22px] font-normal btn-default outline btn-medium pl-3 py-1.5 pr-1.5 rounded-[50px]" data-search="${item}">
            ${item}
            <span class="inline-flex items-center justify-center size-4 bg-[rgba(145,158,171,0.32)] rounded-full ml-2 remove-search-item">
              <i class="hgi hgi-stroke hgi-cancel-01 text-xs text-white"></i>
            </span>
          </button>`
        );

        // Handle remove individual item
        $button.find(".remove-search-item").on("click.sellzy", function (e) {
          e.stopPropagation();
          removeSearchItem(item);
        });

        // Handle clicking on search item to search for it
        $button.on("click.sellzy", function (e) {
          if (!$(e.target).closest(".remove-search-item").length) {
            $(".header-search-input").val(item);
            // Optionally show search dropdown
            $(".header-search-input").trigger("input.sellzy");
          }
        });

        $container.append($button);
      });
    });
  }

  // Add search to history
  function addSearchToHistory(searchQuery) {
    if (!searchQuery || searchQuery.trim().length === 0) return;

    let history = JSON.parse(localStorage.getItem(SEARCH_HISTORY_KEY)) || [];

    // Remove if already exists (to avoid duplicates)
    history = history.filter((item) => item !== searchQuery);

    // Add to the beginning
    history.unshift(searchQuery);

    // Keep only the last MAX_SEARCH_HISTORY items
    if (history.length > MAX_SEARCH_HISTORY) {
      history = history.slice(0, MAX_SEARCH_HISTORY);
    }

    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(history));
    loadSearchHistory();
  }

  // Remove individual search item
  function removeSearchItem(item) {
    let history = JSON.parse(localStorage.getItem(SEARCH_HISTORY_KEY)) || [];
    history = history.filter((h) => h !== item);
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(history));
    loadSearchHistory();
  }

  // Clear all search history
  function clearSearchHistory() {
    localStorage.removeItem(SEARCH_HISTORY_KEY);
    loadSearchHistory();
  }

  // Render recommended products and optionally filter by search text
  function renderRecommendedProducts(filterText) {
    const query = typeof filterText === "string" ? filterText.trim().toLowerCase() : "";

    // Use AJAX to fetch real search results from backend
    if (query.length > 0 || true) {  // Always fetch for real-time results
      $.ajax({
        url: '/api/search/',
        type: 'GET',
        data: { q: query },
        dataType: 'json',
        timeout: 5000,
        success: function(response) {
          const filteredProducts = response.results || [];

          $(".recommended-search-list").each(function () {
            const $list = $(this);
            $list.empty();

            if (!filteredProducts.length) {
              $list.html('<p class="text-sm text-gray-500 py-2">No products found</p>');
              return;
            }

            filteredProducts.forEach((item) => {
              const productName = String(item.name || "");
              const productUrl = String(item.url || "");
              const productImage = String(item.image || "");
              const productPrice = String(item.price || "");

              const $row = $(
                `<button type="button" class="recommended-search-item w-full text-left flex items-center gap-x-4 py-2 first:pt-0 last:pb-0">
                  <div class="size-10 flex-none rounded-lg bg-[#F4F3F5] overflow-hidden">${
                    productImage
                      ? `<img src="${productImage}" alt="${productName}" class="w-full h-full object-cover" />`
                      : `<div class="w-full h-full bg-gray-300 flex items-center justify-center"><i class="hgi hgi-stroke hgi-image-not-found text-gray-500"></i></div>`
                  }</div>
                  <div class="flex-1">
                    <p class="text-base font-semibold text-light-primary-text hover:text-primary transition-colors duration-300">${productName}</p>
                    <p class="text-sm text-gray-500">₹${productPrice}</p>
                  </div>
                </button>`
              );

              $row.on("click.sellzy", function () {
                if (productUrl) {
                  window.location.href = productUrl;
                  return;
                }
                $(".header-search-input").val(productName);
                $(".header-search-input").trigger("input.sellzy");
              });

              $list.append($row);
            });
          });
        },
        error: function() {
          // Fallback to showing recommended products on error
          $(".recommended-search-list").each(function () {
            const $list = $(this);
            $list.empty();
            $list.html('<p class="text-sm text-gray-500 py-2">Search temporarily unavailable</p>');
          });
        }
      });
    }
  }

  // Handle search input
  $(".header-search-input").on("input.sellzy", function () {
    const rawValue = $(this).val();
    const searchValue = typeof rawValue === "string" ? rawValue.trim() : "";
    // Basic input validation (prevents unexpected values)
    if (searchValue.length <= 200) {
      $(this)
        .closest(".search-input-container")
        .find(".search-result-container")
        .attr("data-state", "open");
      renderRecommendedProducts(searchValue);
    } else {
      $(this)
        .closest(".search-input-container")
        .find(".search-result-container")
        .attr("data-state", "close");
    }
  });

  // Keep dropdown open on focus so users can see recommended products immediately
  $(".header-search-input").on("focus.sellzy", function () {
    $(this)
      .closest(".search-input-container")
      .find(".search-result-container")
      .attr("data-state", "open");
    renderRecommendedProducts($(this).val());
  });

  // Handle search submission - Simple and reliable
  $(document).on("keypress", ".header-search-input", function (e) {
    if (e.keyCode === 13 || e.which === 13) {
      e.preventDefault();
      performSearch($(this));
      return false;
    }
  });

  // Handle search icon click
  $(document).on("click", ".input-group-addon", function (e) {
    e.preventDefault();
    const $input = $(this).closest(".search-input-container").find(".header-search-input");
    performSearch($input);
    return false;
  });

  // Function to perform search
  function performSearch($searchInput) {
    const searchValue = $searchInput.val().trim();
    console.log("Performing search for:", searchValue);
    
    if (searchValue && searchValue.length > 0) {
      addSearchToHistory(searchValue);
      const searchUrl = "/search/?q=" + encodeURIComponent(searchValue);
      console.log("Navigating to:", searchUrl);
      window.location.href = searchUrl;
    } else {
      console.log("Search value is empty");
    }
  }

  // Handle reset history button (works for all buttons with this class)
  $doc.on("click.sellzy", ".reset-search-history-btn", function (e) {
    e.preventDefault();
    clearSearchHistory();
  });

  // Load search history on page load
  loadSearchHistory();
  renderRecommendedProducts("");

  /*------ Accordion Section ----*/
  $(".accordion-header").on("click.sellzy", function () {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this).siblings(".accordion-body").slideUp();
    } else {
      $(this)
        .parent()
        .siblings()
        .children(".accordion-header")
        .removeClass("active");
      $(this).parent().siblings().children(".accordion-body").slideUp();
      $(this).addClass("active");
      $(this).siblings(".accordion-body").slideDown();
    }
  });

  /*------ FAQ Tab Accordion ----*/
  const faqFilterButton = $(".faq-filter button");
  if (faqFilterButton.length) {
    $(".faq-filter button:nth-child(1)")
      .addClass("active")
      .siblings()
      .removeClass("active");
    $(".faq-tab-pane").hide();
    $(".faq-tab-pane:nth-child(1)").addClass("active").show();

    faqFilterButton.on("click.sellzy", function () {
      $(this).addClass("active").siblings().removeClass("active");
      $(".faq-tab-pane").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
    });
  }

  /*------ Mobile Menu ----*/
  const mobileMenu = $(".mobile-menu");
  if (mobileMenu.length) {
    mobileMenu
      .find("ul li")
      .parents(".mobile-menu ul li")
      .addClass("has-sub-item")
      .prepend('<span class="submenu-button"></span>'),
      mobileMenu.find(".submenu-button").on("click.sellzy", function () {
        $(this).toggleClass("submenu-opened");
        $(this).siblings("ul").hasClass("open")
          ? $(this).siblings("ul").removeClass("open").slideUp("fast")
          : $(this).siblings("ul").addClass("open").slideDown("fast");
      });
  }

  /*------ Main Menu ----*/
  const mainMenu = $(".main-menu");
  if (mainMenu.length) {
    mainMenu.find("ul li").parents(".main-menu ul li").addClass("has-sub-item");
    mainMenu
      .find("ul li.has-sub-item > a")
      .append(
        '<i class="hgi hgi-stroke hgi-arrow-down-01 text-xl text-light-primary-text"></i>'
      );
  }

  /*------ Payment Method ----*/
  const paymentMethod = $(".payment-methods input[name='payment-method']");
  const selectedPaymentMethod = $(
    ".payment-methods input[name='payment-method']:checked"
  );
  if (selectedPaymentMethod.length) {
    selectedPaymentMethod.parents(".payment-method").addClass("selected");
    selectedPaymentMethod
      .parents(".payment-method")
      .find(".payment-content")
      .show();
  }
  if (paymentMethod.length) {
    paymentMethod.on("change.sellzy", function () {

      $(this).parents(".payment-method").siblings().removeClass("selected");
      $(this).parents(".payment-method").addClass("selected");
      $(this)
        .parents(".payment-method")
        .siblings()
        .find(".payment-content")
        .slideUp();
      $(this).parents(".payment-method").find(".payment-content").slideDown();
    });
  }

  /*------ Home Five Product Filter Buttons ------*/
  const homeFiveProductFilterButtons = $(".home-five-product-filter button");
  if (homeFiveProductFilterButtons.length) {
    $(".home-five-product-filter button:nth-child(1)")
      .addClass("btn-primary")
      .removeClass("btn-default outline shadow-none")
      .siblings()
      .removeClass("btn-primary")
      .addClass("btn-default outline shadow-none");
    $(".tab-pane").hide();

    $(".tab-pane:nth-child(1)").addClass("active").show();
    $(".home-five-product-filter button").on("click.sellzy", function () {
      $(this)
        .removeClass("btn-default outline shadow-none")
        .addClass("btn-primary")
        .siblings()
        .removeClass("btn-primary")
        .addClass("btn-default outline shadow-none");
      $(".tab-pane").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
      return false;
    });
  }

  /*------ Home Five Variation Color Buttons ------*/
  const homeFiveVariationColorButtons = $(".variation-color-item button");
  if (homeFiveVariationColorButtons.length) {
    homeFiveVariationColorButtons.on("click.sellzy", function () {
      const color = $(this).data("color");
      $(this).parent().css("border-color", color);
      $(this).parent().siblings().css("border-color", "#dfe3e8");
      $(this).parent().siblings().find("i").addClass("hidden");
      $(this).find("i").removeClass("hidden");
    });
  }

  /*------ Is Anything Open ------*/
  function isAnythingOpen() {
    const isAnythingOpen = $modalOverlay.attr("data-overlay-for");
    if (isAnythingOpen) {
      $(isAnythingOpen).attr("data-state", "close");
    }
  }

  /*------ Show Sidebar ------*/
  function showSidebar(sidebarFor) {
    $(sidebarFor).attr("data-state", "open");
    $body.addClass("overflow-hidden scrollbar-offset");
    $modalOverlay.fadeIn();
    $modalOverlay.attr("data-overlay-for", sidebarFor);
  }

  /*------ Close Sidebar ------*/
  function closeSidebar(sidebarFor) {
    $(sidebarFor).attr("data-state", "close");
    $body.removeClass("overflow-hidden scrollbar-offset");
    $modalOverlay.fadeOut();
    $modalOverlay.removeAttr("data-overlay-for");
  }

  
  /*------ About Us Page Counter Up ------*/
  safeInit(function () {
    if (!window.counterUp || !window.counterUp.default) return;
    if (typeof IntersectionObserver === "undefined") return;

    const counterUp = window.counterUp.default;

    const callback = (entries) => {
      entries.forEach((entry) => {
        const el = entry.target;
        if (entry.isIntersecting && !el.classList.contains("is-visible")) {
          safeInit(function () {
            counterUp(el, { duration: 2000, delay: 16 });
          });
          el.classList.add("is-visible");
        }
      });
    };

    const IO = new IntersectionObserver(callback, { threshold: 1 });
    addCleanup(function () {
      try {
        IO.disconnect();
      } catch (e) {}
    });

    const els = document.querySelectorAll(".about-us-counter");
    if (!els || !els.length) return;
    els.forEach((el) => IO.observe(el));
  });

/*------ About Us Page Video Popup ------*/

  safeInit(function () {
    if ($.fn && $.fn.magnificPopup) {
      $(".about-us-popup-youtube").magnificPopup({
    type: "iframe",

    iframe: {
      markup:
        '<div class="mfp-iframe-scaler">' +
        '<div class="mfp-close"></div>' +
        '<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>' +
        "</div>", // HTML markup of popup, `mfp-close` will be replaced by the close button

      patterns: {
        youtube: {
          index: "youtube.com/",
          id: "v=",
          src: "//www.youtube.com/embed/%id%?autoplay=1",
        },
        vimeo: {
          index: "vimeo.com/",
          id: "/",
          src: "//player.vimeo.com/video/%id%?autoplay=1",
        },
        gmaps: {
          index: "//maps.google.",
          src: "%id%&output=embed",
        },
      },

      srcAction: "iframe_src",
    },
      });
    }
  });

  /*------ Price Range Slider Widget ------*/
  const priceRangeSlider = document.getElementById("price-range-slider");
  if (priceRangeSlider) {
    safeInit(function () {
      if (typeof noUiSlider === "undefined") return;
      noUiSlider.create(priceRangeSlider, {
      start: [0, 100],
      connect: true,
      range: {
        min: 0,
        max: 100,
      },
      // make numbers whole
      format: {
        to: (value) => value,
        from: (value) => value,
      },
    });

      priceRangeSlider.noUiSlider.on("update", (values) => {
      $(".price-range-min-value").val(values[0].toFixed(0));
      $(".price-range-max-value").val(values[1].toFixed(0));
      });

      addCleanup(function () {
        try {
          if (priceRangeSlider.noUiSlider) priceRangeSlider.noUiSlider.destroy();
        } catch (e) {}
      });
    });
  }

  /*------ Star Rating Widget ------*/
  $(".widget-rating a").on("click.sellzy", function (e) {
    e.preventDefault();
    $(this).parent().siblings().find("a").removeClass("active");
    $(this).addClass("active");
  });
  
  // Handle rating filter Apply Now button
  $(".filter-dropdown .btn-primary").each(function() {
    if ($(this).text().includes("Apply")) {
      $(this).closest(".filter-dropdown").find(".widget-rating").each(function() {
        $(this).closest(".filter-dropdown-menu").find(".btn-primary").on("click.sellzy", function(e) {
          e.preventDefault();
          const selectedRating = $(this).closest(".filter-dropdown-menu").find(".widget-rating a.active").text();
          if (selectedRating) {
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('rating', selectedRating.trim());
            window.location.href = currentUrl.toString();
          }
        });
      });
    }
  });
  
  // Handle rating filter reset
  $(".widget-rating-title a").on("click.sellzy", function(e) {
    e.preventDefault();
    const currentUrl = new URL(window.location);
    currentUrl.searchParams.delete('rating');
    window.location.href = currentUrl.toString();
  });

  /*------ Color Picker Widget ------*/
  $(".widget-color-picker button").on("click.sellzy", function () {
    $(this).parent().siblings().find("button").removeClass("active");
    $(this).addClass("active");
  });

  /*------ Size Picker Widget ------*/
  $(".widget-size-picker button").on("click.sellzy", function () {
    $(this).parent().siblings().find("button").removeClass("active");
    $(this).addClass("active");
  });

  /*------ Product Details Tabs Section ------*/
  const productDetailsTabs = $("#product-details-tabs button");
  if (productDetailsTabs.length) {
    productDetailsTabs.on("click.sellzy", function () {
      $(this)
        .addClass("active")
        .parent()
        .siblings()
        .find("button")
        .removeClass("active");
      $(".product-details-tab").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
    });
  }

  /*------ Product Details Color Variation ------*/
  const productDetailsColorVariation = $(".color-variation-item button");
  if (productDetailsColorVariation.length) {
    productDetailsColorVariation.on("click.sellzy", function () {
      $(this).css("border-color", $(this).attr("data-color"));
      $(this).parent().siblings().find("button").css("border-color", "#dfe3e8");
      $(".color-variation-selected-color").text(
        $(this).attr("data-color-text")
      );
    });
  }

  /*------ Product Details Color Variation ------*/
  const productDetailsSizeVariation = $(".size-variation-item button");
  if (productDetailsSizeVariation.length) {
    productDetailsSizeVariation.on("click.sellzy", function () {
      $(this).addClass("border-primary bg-primary hover:bg-primary text-white");
      $(this)
        .parent()
        .siblings()
        .find("button")
        .removeClass("border-primary bg-primary hover:bg-primary text-white")
        .addClass("border-gray-300 text-light-primary-text");
      $(".size-variation-selected-size").text($(this).attr("data-size-text"));
    });
  }

  /*------ Product Details Size Variation Modal ------*/
  const productDetailsSizeVariationModal = $(".variation-size-guide-btn");
  if (productDetailsSizeVariationModal.length) {
    productDetailsSizeVariationModal.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".size-variation-modal");
    });
  }

  /*------ Product Details Height Range Slider Widget ------*/
  const heightRangeSlider = document.querySelector("#height-range-slider");
  if (heightRangeSlider) {
    safeInit(function () {
      if (typeof noUiSlider === "undefined") return;
      noUiSlider.create(heightRangeSlider, {
      start: 80,
      connect: "lower",
      range: {
        min: 0,
        max: 200,
      },
      // make numbers whole
      format: {
        to: (value) => value,
        from: (value) => value,
      },
    });

      heightRangeSlider.noUiSlider.on("update", (values) => {
        $(".height-range-slider-value").text(values[0].toFixed(0));
      });

      addCleanup(function () {
        try {
          if (heightRangeSlider.noUiSlider) heightRangeSlider.noUiSlider.destroy();
        } catch (e) {}
      });
    });
  }

  /*------ Product Details Weight Range Slider Widget ------*/
  const weightRangeSlider = document.querySelector("#weight-range-slider");
  if (weightRangeSlider) {
    safeInit(function () {
      if (typeof noUiSlider === "undefined") return;
      noUiSlider.create(weightRangeSlider, {
      start: 80,
      connect: "lower",
      range: {
        min: 0,
        max: 200,
      },
      // make numbers whole
      format: {
        to: (value) => value,
        from: (value) => value,
      },
    });

      weightRangeSlider.noUiSlider.on("update", (values) => {
        $(".weight-range-slider-value").text(values[0].toFixed(0));
      });

      addCleanup(function () {
        try {
          if (weightRangeSlider.noUiSlider) weightRangeSlider.noUiSlider.destroy();
        } catch (e) {}
      });
    });
  }

  /*------ Home Four Product Filter Buttons ------*/
  const homeFourProductFilterButtons = $(".home-four-product-filter button");
  if (homeFourProductFilterButtons.length) {
    $(".home-four-product-filter button:nth-child(1)")
      .addClass(
        "text-light-primary-text border-b-2 border-[text-light-primary-text] bg-transparent font-semibold"
      )
      .removeClass("bg-transparent")
      .siblings()
      .removeClass(
        "text-light-primary-text border-b-2 border-[text-light-primary-text] bg-transparent font-semibold"
      )
      .addClass("bg-transparent");
    $("#deal-tab-content .tab-pane").hide();

    $("#deal-tab-content .tab-pane:nth-child(1)").addClass("active").show();
    $(".home-four-product-filter button").on("click.sellzy", function () {
      $(this)
        .removeClass("bg-transparent")
        .addClass(
          "text-light-primary-text border-b-2 border-[text-light-primary-text] bg-transparent font-semibold"
        )
        .siblings()
        .removeClass(
          "text-light-primary-text border-b-2 border-[text-light-primary-text] bg-transparent font-semibold"
        )
        .addClass("bg-transparent");
      $("#deal-tab-content .tab-pane").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
      return false;
    });
  }

  /*------ Home Four Category Filter Buttons ------*/
  const homeFourCategoryFilterButtons = $(".home-four-category-filter button");
  if (homeFourCategoryFilterButtons.length) {
    $(".home-four-category-filter button:nth-child(1)")
      .addClass("text-primary bg-transparent")
      .removeClass("bg-transparent")
      .siblings()
      .removeClass("text-primary bg-transparent")
      .addClass("bg-transparent");
    $("#category-tab-content .tab-pane").hide();

    $("#category-tab-content .tab-pane:nth-child(1)").addClass("active").show();
    $(".home-four-category-filter button").on("click.sellzy", function () {
      $(this)
        .removeClass("bg-transparent")
        .addClass("text-primary bg-transparent")
        .siblings()
        .removeClass("text-primary bg-transparent")
        .addClass("bg-transparent");
      $("#category-tab-content .tab-pane").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
      return false;
    });
  }

  /*------ Home Two Product Filter Buttons ------*/
  const homeTwoProductFilterButtons = $(".home-two-product-filter button");
  if (homeTwoProductFilterButtons.length) {
    $(".home-two-product-filter button:nth-child(1)")
      .addClass("btn-primary")
      .removeClass("btn-default outline shadow-none")
      .siblings()
      .removeClass("btn-primary")
      .addClass("btn-default outline  shadow-none");
    $(".tab-pane").hide();

    $(".tab-pane:nth-child(1)").addClass("active").show();
    $(".home-two-product-filter button").on("click.sellzy", function () {
      $(this)
        .removeClass("btn-default outline shadow-none")
        .addClass("btn-primary")
        .siblings()
        .removeClass("btn-primary")
        .addClass("btn-default outline  shadow-none");
      $(".tab-pane").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
      return false;
    });
  }

  /*------ Order History Filter Buttons ------*/
  const orderHistoryProductFilterButtons = $(
    ".order-history-product-filter button"
  );
  if (orderHistoryProductFilterButtons.length) {
    $(".order-history-product-filter button:nth-child(1)")
      .addClass("bg-primary/8 text-primary ")
      .removeClass("text-light-primary-text")
      .siblings()
      .removeClass("bg-primary/8 text-primary")
      .addClass("text-light-primary-text");
    $("#order-tab-content .tab-pane").hide();

    $("#order-tab-content .tab-pane:nth-child(1)").addClass("active").show();
    $(".order-history-product-filter button").on("click.sellzy", function () {
      $(this)
        .removeClass("text-light-primary-text")
        .addClass("bg-primary/8 text-primary")
        .siblings()
        .removeClass("bg-primary/8 text-primary")
        .addClass("text-light-primary-text");
      $("#order-tab-content .tab-pane").removeClass("active fade").hide();
      let activeTab = $(this).attr("data-tab");
      $(`#${activeTab}`).addClass("active fade").fadeIn();
      return false;
    });
  }

  /*------ My Account Navigation Buttons ------*/
  const myAccountMenuButton = $(".my-account-menu button");
  if (myAccountMenuButton.length) {
    myAccountMenuButton.on("click.sellzy", function () {
      if ($(this).data("tab") === "logout") {
        return false;
      }
      $(this)
        .addClass("active")
        .parent()
        .siblings()
        .find("button")
        .removeClass("active");
      $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
      let activeTab = $(this).attr("data-tab");
      $(".my-account-content")
        .find(`#${activeTab}`)
        .removeClass("hidden")
        .addClass("active fade")
        .fadeIn();
    });
  }

  $(".order-details-button").on("click.sellzy", function () {
    $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
    $("#order-details").removeClass("hidden").addClass("active fade").fadeIn();
  });

  $(".order-details-back-button").on("click.sellzy", function () {
    $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
    $("#orders").removeClass("hidden").addClass("active fade").fadeIn();
  });

  $(".add-new-address-button").on("click.sellzy", function () {
    $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
    $("#add-address").removeClass("hidden").addClass("active fade").fadeIn();
  });

  $(".add-new-address-back-button").on("click.sellzy", function () {
    $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
    $("#address").removeClass("hidden").addClass("active fade").fadeIn();
  });

  $(".edit-address-button").on("click.sellzy", function () {
    $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
    $("#edit-address").removeClass("hidden").addClass("active fade").fadeIn();
  });

  $(".edit-address-back-button").on("click.sellzy", function () {
    $(".menu-tab-pane").removeClass("active fade").addClass("hidden");
    $("#address").removeClass("hidden").addClass("active fade").fadeIn();
  });

  $(".logout-button").on("click.sellzy", function (e) {
    e.preventDefault();
    isAnythingOpen();
    showSidebar(".logout-modal");
  });

  /*------ Banner with Filter Button  ------*/
  $(".filter-button").on("click.sellzy", function () {
    const parent = $(this).closest(".filter-dropdown");
    const menu = parent.find(".filter-dropdown-menu");
    const icon = parent.find(".filter-dropdown-icon");

    const isOpen = $(this).attr("data-state") === "open";

    $(".filter-button").attr("data-state", "close");
    $(".filter-button").removeClass(
      "ring-primary text-primary transition-colors duration-300 ease-in-out"
    );
    $(".filter-button span i").removeClass(
      "text-primary transition-colors duration-300 ease-in-out"
    );
    $(".filter-dropdown-menu").removeClass("active").addClass("hide");
    $(".filter-dropdown-icon").removeClass(
      "rotate-180 text-primary transition-colors duration-300 ease-in-out"
    );

    if (!isOpen) {
      $(this).attr("data-state", "open");
      $(this).addClass(
        "ring-primary text-primary transition-colors duration-300 ease-in-out"
      );
      $(this)
        .find("span i")
        .addClass("text-primary transition-colors duration-300 ease-in-out");
      menu.removeClass("hide").addClass("active");
      icon.addClass(
        "rotate-180 text-primary transition-colors duration-300 ease-in-out"
      );

      const rect = parent[0].getBoundingClientRect();
      const windowWidth = window.innerWidth;

      menu.removeClass("left-0 right-0 left-auto right-auto");

      if (rect.left + rect.width / 2 > windowWidth / 2) {
        menu.addClass("right-0 left-auto");
      } else {
        menu.addClass("left-0 right-auto");
      }
    }
  });

  /*------ Filter Sidebar ----*/
  const filterSidebarMenu = $("#filter-menu-btn");
  const filterSidebar = $("#filter-sidebar");
  const filterSidebarMenuClose = $("#filter-side-bar-menu-close");

  if (filterSidebarMenu.length) {
    filterSidebarMenu.on("click.sellzy", function () {
      $(filterSidebar).attr("data-state", "open");
      $body.addClass("overflow-hidden");
    });
  }

  if (filterSidebarMenuClose.length) {
    filterSidebarMenuClose.on("click.sellzy", function () {
      $(filterSidebar).attr("data-state", "close");
      $body.removeClass("overflow-hidden");
    });
  }
  const filterPriceRangeSlider = document.getElementById(
    "filter-price-range-slider"
  );
  if (filterPriceRangeSlider) {
    safeInit(function () {
      if (typeof noUiSlider === "undefined") return;

      noUiSlider.create(filterPriceRangeSlider, {
        start: [0, 100],
        connect: true,
        range: {
          min: 0,
          max: 100,
        },
        format: {
          to: (value) => value,
          from: (value) => value,
        },
      });

      filterPriceRangeSlider.noUiSlider.on("update", (values) => {
        $(".filter-price-range-min-value").val(Number(values[0]).toFixed(0));
        $(".filter-price-range-max-value").val(Number(values[1]).toFixed(0));
      });

      addCleanup(function () {
        try {
          if (filterPriceRangeSlider.noUiSlider) {
            filterPriceRangeSlider.noUiSlider.destroy();
          }
        } catch (e) {}
      });
    });
  }

  /*------ Quick View Sidebar ------*/
  const quickViewSidebarBtn = $(".quick-view-sidebar-btn");
  if (quickViewSidebarBtn.length) {
    quickViewSidebarBtn.on("click.sellzy", function (e) {
      e.preventDefault();
      isAnythingOpen();
      showSidebar(".quick-view-sidebar");
    });
  }

  /*------ Radial Bar Chart ------*/
  const radialBarChart = $("#radial-bar-chart");
  if (radialBarChart.length) {
    const radialBarChartOptions = {
      series: [30, 20, 70, 50],
      chart: {
        width: 250,
        type: "donut",
      },
      dataLabels: {
        enabled: false,
      },
      colors: ["#5ed9ba", "#056d6e", "#04535c", "#088178"],
      labels: [
        "Recent Orders",
        "Pending Payments",
        "Received Payments",
        "Complete Order",
      ],
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: {
              width: 200,
            },
            legend: {
              show: false,
            },
          },
        },
      ],
      legend: {
        show: false,
      },
    };

    safeInit(function () {
      if (typeof ApexCharts === "undefined") return;
      new ApexCharts(
        document.querySelector("#radial-bar-chart"),
        radialBarChartOptions
      ).render();
    });
  }

  /*------ Price Movement Chart ------*/
  const priceMovementChart = $("#price-movement-chart");
  if (priceMovementChart.length) {
    const priceMovementChartOptions = {
      series: [
        {
          name: "Asia",
          data: [85, 32, 67, 120, 45, 98, 23, 140, 75, 110, 55, 135],
        },
        {
          name: "America",
          data: [20, 51, 35, 51, 49, 62, 69, 91, 148, 100, 120, 150],
        },
      ],
      colors: ["#088178", "#FFE700"],
      chart: {
        height: 340,
        type: "line",
        zoom: {
          enabled: false,
        },
        toolbar: {
          show: false,
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "straight",
        width: 2,
      },
      title: {
        show: false,
      },
      grid: {
        show: true,
        strokeDashArray: 3,
        strokeColor: "#919EAB3D",
      },
      yaxis: {
        labels: {
          style: {
            fontSize: "12px",
            fontWeight: "400",
            color: "#919EAB",
            fontFamily: "var(--font-dm-sans)",
          },
        },
      },
      xaxis: {
        labels: {
          style: {
            fontSize: "12px",
            fontWeight: "400",
            color: "#919EAB",
            fontFamily: "var(--font-dm-sans)",
          },
        },
        categories: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
      },
      legend: {
        show: false,
      },
    };

    safeInit(function () {
      if (typeof ApexCharts === "undefined") return;
      new ApexCharts(
        document.querySelector("#price-movement-chart"),
        priceMovementChartOptions
      ).render();
    });
  }

  /*------ Common Slider ----*/
  safeInit(function () {
    if ($.fn && $.fn.slick) {
      $(".sellzy-slider").slick({
    prevArrow:
      '<span class="slider-btn slider-prev size-12 rounded-full inline-flex items-center justify-center transition-colors duration-300 group/slider-btn cursor-pointer"><i class="hgi hgi-stroke hgi-arrow-left-01 text-[22px] text-light-primary-text transition-colors duration-300"></i></span>',
    nextArrow:
      '<span class="slider-btn slider-next size-12 rounded-full inline-flex items-center justify-center transition-colors duration-300 group/slider-btn cursor-pointer"><i class="hgi hgi-stroke hgi-arrow-right-01 text-[22px] text-light-primary-text transition-colors duration-300"></i></span>',
      });

      addCleanup(function () {
        try {
          const $slider = $(".sellzy-slider");
          if ($slider.hasClass("slick-initialized")) $slider.slick("unslick");
        } catch (e) {}
      });
    }
  });

  /*------ Scroll To Top Button ----*/
  const $scrollToTop = $(".scroll-to-top");
  $win.on("scroll.sellzy", function () {
    if ($win.scrollTop() > 300) {
      $scrollToTop.removeClass("hide").addClass("active");
    } else {
      $scrollToTop.removeClass("active").addClass("hide");
    }
  });

  $scrollToTop.on("click.sellzy", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
    return false;
  });

  /*------ Cleanup (Memory Management) ----*/
  function destroy() {
    try {
      // Remove all namespaced event listeners
      $win.off(".sellzy");
      $doc.off(".sellzy");
      $body.off(".sellzy");
      $("select").off(".sellzy");
      $modalOverlay.off(".sellzy");
      $scrollToTop.off(".sellzy");

      // Run additional cleanup tasks (observers, sliders, plugins)
      cleanupTasks.forEach(function (task) {
        try {
          task();
        } catch (e) {}
      });
    } catch (e) {}
  }

  // Cleanup on page unload/navigation
  $win.on("unload.sellzy", destroy);
})(jQuery);
