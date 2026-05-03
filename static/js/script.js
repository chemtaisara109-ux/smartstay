/**
 * SmartStay JavaScript
 * Modern frontend functionality for Airbnb-style booking platform
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// ==================== APP INITIALIZATION ====================
function initializeApp() {
    setupNavigation();
    setupSearchForm();
    setupPropertyCards();
    setupFlashMessages();
    setupFormValidation();
    setupImageLazyLoading();
}

// ==================== NAVIGATION ====================
function setupNavigation() {
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !mobileMenuToggle.contains(e.target)) {
                navMenu.classList.remove('active');
                mobileMenuToggle.classList.remove('active');
            }
        });
    }

    const dropdownButtons = document.querySelectorAll('.nav-dropdown-btn');
    dropdownButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const dropdown = this.closest('.nav-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('active');
            }
        });
    });

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-dropdown')) {
            document.querySelectorAll('.nav-dropdown.active').forEach(dropdown => dropdown.classList.remove('active'));
        }
    });

    // Sticky navigation
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                navbar.classList.add('sticky');
            } else {
                navbar.classList.remove('sticky');
            }
        });
    }
}

// ==================== SEARCH FORM ====================
function setupSearchForm() {
    const searchForm = document.querySelector('.search-form');
    if (!searchForm) return;

    const locationInput = document.getElementById('location');
    const mapPanel = document.getElementById('searchMapPanel');
    const openMapToggle = document.getElementById('openMapToggle');
    const destinationChips = document.querySelectorAll('.destination-chip');
    const mapPins = document.querySelectorAll('.map-pin');

    if (openMapToggle && mapPanel) {
        openMapToggle.addEventListener('click', function() {
            mapPanel.classList.toggle('visible');
        });
    }

    destinationChips.forEach(chip => {
        chip.addEventListener('click', function() {
            if (locationInput) {
                locationInput.value = this.dataset.location;
            }
            destinationChips.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
        });
    });

    mapPins.forEach(pin => {
        pin.addEventListener('click', function() {
            if (locationInput) {
                locationInput.value = this.dataset.location;
            }
            if (mapPanel) {
                mapPanel.classList.add('visible');
            }
        });
    });

    // Date validation
    const checkinInput = document.getElementById('checkin');
    const checkoutInput = document.getElementById('checkout');

    if (checkinInput && checkoutInput) {
        const today = new Date().toISOString().split('T')[0];
        checkinInput.min = today;
        checkoutInput.min = today;

        checkinInput.addEventListener('change', function() {
            checkoutInput.min = this.value;
            if (checkoutInput.value && checkoutInput.value <= this.value) {
                checkoutInput.value = '';
            }
        });

        checkoutInput.addEventListener('change', function() {
            if (checkinInput.value && this.value <= checkinInput.value) {
                this.value = '';
            }
        });
    }

    // Form submission
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(this);
        const searchParams = new URLSearchParams();

        for (let [key, value] of formData.entries()) {
            if (value.trim()) {
                searchParams.append(key, value);
            }
        }

        // Redirect to search results
        window.location.href = `/search?${searchParams.toString()}`;
    });
}

// ==================== PROPERTY CARDS ====================
function setupPropertyCards() {
    const propertyCards = document.querySelectorAll('.property-card');

    propertyCards.forEach(card => {
        // Heart button functionality
        const heartBtn = card.querySelector('.property-heart');
        if (heartBtn) {
            heartBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                this.classList.toggle('liked');
                const icon = this.querySelector('i');
                if (icon) {
                    icon.className = this.classList.contains('liked') ? 'fas fa-heart' : 'far fa-heart';
                }
            });
        }

        // Card click navigation
        card.addEventListener('click', function() {
            const propertyId = this.dataset.propertyId;
            if (propertyId) {
                window.location.href = `/property/${propertyId}`;
            }
        });
    });
}

// ==================== FLASH MESSAGES ====================
function setupFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(message => {
        // Auto-hide after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);

        // Close button
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
    });
}

// ==================== FORM VALIDATION ====================
function setupFormValidation() {
    // Password confirmation validation
    const confirmPasswordInputs = document.querySelectorAll('input[name="confirm_password"]');
    confirmPasswordInputs.forEach(input => {
        input.addEventListener('input', function() {
            const password = document.querySelector('input[name="password"]').value;
            const confirmPassword = this.value;

            if (confirmPassword && password !== confirmPassword) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    });

    // Real-time email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const email = this.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (email && !emailRegex.test(email)) {
                showFieldError(this, 'Please enter a valid email address');
            } else {
                hideFieldError(this);
            }
        });
    });

    // Form submission with loading states
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

                // Re-enable after 10 seconds (fallback)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.dataset.originalText || 'Submit';
                }, 10000);
            }
        });
    });
}

// ==================== IMAGE LAZY LOADING ====================
function setupImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// ==================== UTILITY FUNCTIONS ====================

// Show field error
function showFieldError(field, message) {
    hideFieldError(field);

    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;

    field.parentNode.appendChild(errorDiv);
    field.classList.add('error');
}

// Hide field error
function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.classList.remove('error');
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format currency
function formatCurrency(amount, currency = 'KES') {
    return new Intl.NumberFormat('en-KE', {
        style: 'currency',
        currency: currency,
    }).format(amount);
}

// Format date
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };

    return new Date(date).toLocaleDateString('en-US', {...defaultOptions, ...options });
}

// Calculate nights between dates
function calculateNights(checkin, checkout) {
    const checkinDate = new Date(checkin);
    const checkoutDate = new Date(checkout);
    const diffTime = Math.abs(checkoutDate - checkinDate);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

// ==================== BOOKING SYSTEM ====================

// Initialize booking calendar
function initializeBookingCalendar(propertyId, bookedDates = []) {
    // This would integrate with a calendar library like FullCalendar
    // For now, we'll use basic date inputs with validation
    const checkinInput = document.getElementById('booking-checkin');
    const checkoutInput = document.getElementById('booking-checkout');

    if (checkinInput && checkoutInput) {
        // Disable already booked dates
        const today = new Date().toISOString().split('T')[0];
        checkinInput.min = today;

        checkinInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const nextDay = new Date(selectedDate);
            nextDay.setDate(selectedDate.getDate() + 1);

            checkoutInput.min = nextDay.toISOString().split('T')[0];
            checkoutInput.value = '';

            updateBookingSummary();
        });

        checkoutInput.addEventListener('change', function() {
            updateBookingSummary();
        });
    }
}

// Update booking summary
function updateBookingSummary() {
    const checkinElement = document.getElementById('booking-checkin');
    const checkoutElement = document.getElementById('booking-checkout');
    const guestsElement = document.getElementById('booking-guests');
    const pricePerNightElement = document.getElementById('price-per-night');

    const checkin = checkinElement ? checkinElement.value : null;
    const checkout = checkoutElement ? checkoutElement.value : null;
    const guests = guestsElement ? guestsElement.value : null;
    const pricePerNight = parseFloat(pricePerNightElement ? pricePerNightElement.dataset.price || 0 : 0);

    if (checkin && checkout && pricePerNight > 0) {
        const nights = calculateNights(checkin, checkout);
        const subtotal = nights * pricePerNight;
        const serviceFee = Math.round(subtotal * 0.14); // 14% service fee
        const total = subtotal + serviceFee;

        // Update summary display
        document.getElementById('nights-count').textContent = nights;
        document.getElementById('subtotal-amount').textContent = formatCurrency(subtotal);
        document.getElementById('service-fee-amount').textContent = formatCurrency(serviceFee);
        document.getElementById('total-amount').textContent = formatCurrency(total);
    }
}

// ==================== MODALS & OVERLAYS ====================

// Show modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        // Close on overlay click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideModal(modalId);
            }
        });
    }
}

// Hide modal
function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// ==================== API CALLS ====================

// Generic API call function
async function apiCall(endpoint, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };

    try {
        const response = await fetch(endpoint, {...defaultOptions, ...options });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'API call failed');
        }

        return data;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Search properties
async function searchProperties(query) {
    try {
        const response = await apiCall('/api/search', {
            method: 'POST',
            body: JSON.stringify(query)
        });
        return response;
    } catch (error) {
        console.error('Search error:', error);
        return [];
    }
}

// ==================== RESPONSIVE UTILITIES ====================

// Check if device is mobile
function isMobile() {
    return window.innerWidth <= 768;
}

// Handle window resize
window.addEventListener('resize', debounce(function() {
    // Close mobile menu on desktop
    if (!isMobile()) {
        const navMenu = document.querySelector('.nav-menu');
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');

        if (navMenu) navMenu.classList.remove('active');
        if (mobileMenuToggle) mobileMenuToggle.classList.remove('active');
    }
}, 250));

// ==================== ACCESSIBILITY ====================

// Keyboard navigation for dropdowns
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close all modals and dropdowns
        const modals = document.querySelectorAll('.modal[style*="display: flex"]');
        modals.forEach(modal => modal.style.display = 'none');

        const dropdowns = document.querySelectorAll('.nav-dropdown.open');
        dropdowns.forEach(dropdown => dropdown.classList.remove('open'));
    }
});

// Focus management
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input[type="text"], input[type="email"], input[type="password"], select'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
    });
}

// ==================== PERFORMANCE ====================

// Preload critical images
function preloadCriticalImages() {
    const criticalImages = [
        '/static/images/hero-bg.jpg',
        '/static/images/logo.png'
    ];

    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Initialize performance optimizations
if ('requestIdleCallback' in window) {
    requestIdleCallback(preloadCriticalImages);
} else {
    setTimeout(preloadCriticalImages, 1000);
}

// ==================== ERROR HANDLING ====================

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send to error tracking service
});

// Unhandled promise rejections
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // Could send to error tracking service
});

// ==================== ANALYTICS (OPTIONAL) ====================

// Track page views
function trackPageView(page) {
    // This would integrate with analytics service like Google Analytics
    console.log('Page view:', page);
}

// Track user interactions
function trackEvent(event, data) {
    // This would send events to analytics service
    console.log('Event:', event, data);
}

// Initialize analytics
document.addEventListener('DOMContentLoaded', function() {
    trackPageView(window.location.pathname);
});

// ==================== HAMBURGER MENU ====================
function setupHamburgerMenu() {
    const hamburger = document.querySelector('.hamburger-menu');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });

        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }

    // Setup dropdown menus
    const dropdowns = document.querySelectorAll('.nav-dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.nav-link');
        if (toggle) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                dropdown.classList.toggle('open');
            });
        }
    });
}

// ==================== LOCATION MAP ====================
function toggleLocationMap() {
    const mapContainer = document.getElementById('location-map');
    if (!mapContainer) return;

    if (mapContainer.style.display === 'none' || mapContainer.style.display === '') {
        mapContainer.style.display = 'block';
        setTimeout(() => {
            if (!map) {
                initializeMap();
            }
            map.invalidateSize();
        }, 100);
    } else {
        mapContainer.style.display = 'none';
    }
}

function initializeMap() {
    if (map) return;

    const mapContainer = document.getElementById('location-map');
    map = L.map(mapContainer).setView([-0.3667, 36.6753], 7); // Kenya center

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);

    // Add predefined locations
    const locations = [
        { name: 'Nanyuki', lat: 0.0019, lng: 37.0699 },
        { name: 'Nyahururu', lat: 0.5412, lng: 36.7633 },
        { name: 'Thomson Falls', lat: 0.6833, lng: 36.6167 },
        { name: 'Ewaso Nyiro River', lat: 0.35, lng: 37.2 },
        { name: 'Olekalao', lat: 0.45, lng: 37.15 }
    ];

    locations.forEach(location => {
        const markerIcon = L.icon({
            iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/svgs/solid/location-dot.svg',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34]
        });

        const mapMarker = L.marker([location.lat, location.lng], { icon: markerIcon }).addTo(map);
        mapMarker.bindPopup(`<b>${location.name}</b><br><button onclick="selectLocation('${location.name}')">Select</button>`);
    });

    // Click on map to select location
    map.on('click', function(e) {
        const locationInput = document.getElementById('location');
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(map);

        // Get location name from coordinates (reverse geocoding)
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${e.latlng.lat}&lon=${e.latlng.lng}`)
            .then(response => response.json())
            .then(data => {
                const locationName = (data.address && (data.address.city || data.address.town || data.address.county)) || 'Selected Location';
                locationInput.value = locationName;
            })
            .catch(() => {
                locationInput.value = `${e.latlng.lat.toFixed(4)}, ${e.latlng.lng.toFixed(4)}`;
            });
    });
}

function selectLocation(locationName) {
    document.getElementById('location').value = locationName;
    document.getElementById('location-map').style.display = 'none';
}

// ==================== DATE PICKERS ====================
function initializeDatePickers() {
    const checkInInput = document.getElementById('check-in');
    const checkOutInput = document.getElementById('check-out');

    if (checkInInput) {
        flatpickr(checkInInput, {
            minDate: 'today',
            onChange: function(selectedDates) {
                if (selectedDates[0] && checkOutInput) {
                    const minCheckOut = new Date(selectedDates[0]);
                    minCheckOut.setDate(minCheckOut.getDate() + 1);
                    flatpickr(checkOutInput, {
                        minDate: minCheckOut
                    });
                }
            }
        });
    }

    if (checkOutInput) {
        flatpickr(checkOutInput, {
            minDate: new Date(new Date().setDate(new Date().getDate() + 1))
        });
    }
}

// ==================== SEARCH FORM ====================
function setupLegacySearchForm() {
    const form = document.getElementById('search-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const location = document.getElementById('location').value;
            const checkIn = document.getElementById('check-in').value;
            const checkOut = document.getElementById('check-out').value;
            const guests = document.getElementById('guests').value;

            if (!location || !checkIn || !checkOut) {
                alert('Please fill in all search fields');
                return;
            }

            if (new Date(checkIn) >= new Date(checkOut)) {
                alert('Check-out date must be after check-in date');
                return;
            }

            // Send search data to backend
            sendSearchToBackendLegacy(location, checkIn, checkOut, guests);
        });
    }
}

function sendSearchToBackendLegacy(location, checkIn, checkOut, guests) {
    showLoader();

    fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                check_in: checkIn,
                check_out: checkOut,
                guests: guests
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoader();
            if (data.success) {
                // Redirect to search results or display results
                window.location.href = `/search?location=${location}&check_in=${checkIn}&check_out=${checkOut}&guests=${guests}`;
            } else {
                alert('No properties found for your search');
            }
        })
        .catch(error => {
            hideLoader();
            console.error('Search error:', error);
            alert('Error performing search. Please try again.');
        });
}

// ==================== UTILITY FUNCTIONS ====================

// Initialize event listeners
function initializeEventListeners() {
    const alerts = document.querySelectorAll('.alert, .error, .success');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('en-KE', {
        style: 'currency',
        currency: 'KES'
    }).format(value);
}

// Validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password strength
function getPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    return strength;
}

// Date validation
function isValidDateRange(checkIn, checkOut) {
    const checkInDate = new Date(checkIn);
    const checkOutDate = new Date(checkOut);
    return checkOutDate > checkInDate;
}

// Calculate nights between dates
function calculateNights(checkIn, checkOut) {
    const checkInDate = new Date(checkIn);
    const checkOutDate = new Date(checkOut);
    const timeDifference = checkOutDate - checkInDate;
    return Math.ceil(timeDifference / (1000 * 3600 * 24));
}

// Calculate total price
function calculateTotalPrice(pricePerNight, nights) {
    return pricePerNight * nights;
}

// Photo preview with multiple uploads
function handlePhotoPreview(input) {
    const preview = document.getElementById('photo-preview');
    if (!preview) return;

    preview.innerHTML = '';
    const files = input.files;

    if (files.length > 5) {
        alert('Maximum 5 photos allowed');
        input.value = '';
        return;
    }

    const previews = [];
    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        if (!file.type.startsWith('image/')) {
            alert('Please select only image files');
            continue;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert(`File ${file.name} is too large (max 5MB)`);
            continue;
        }

        const reader = new FileReader();

        reader.onload = function(e) {
            const container = document.createElement('div');
            container.className = 'photo-preview-item';
            container.style.cssText = 'display: inline-block; position: relative; margin-right: 10px; margin-bottom: 10px;';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = `Photo ${i + 1}`;
            img.style.cssText = 'width: 100px; height: 100px; object-fit: cover; border-radius: 8px;';

            const removeBtn = document.createElement('button');
            removeBtn.innerHTML = '<i class="fas fa-times"></i>';
            removeBtn.type = 'button';
            removeBtn.className = 'remove-photo';
            removeBtn.style.cssText = 'position: absolute; top: -8px; right: -8px; width: 24px; height: 24px; border-radius: 50%; background: #ff385c; color: white; border: none; cursor: pointer;';
            removeBtn.onclick = function() {
                container.remove();
            };

            container.appendChild(img);
            container.appendChild(removeBtn);
            preview.appendChild(container);
        };

        reader.readAsDataURL(file);
    }
}

// Smooth scroll
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Confirm action
function confirmAction(message) {
    return confirm(message);
}

// Show loading spinner
function showLoader() {
    let loader = document.getElementById('loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loader';
        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;
        loader.innerHTML = `
            <div style="
                border: 4px solid #f3f3f3;
                border-top: 4px solid #ff385c;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
            "></div>
        `;
        document.body.appendChild(loader);
    }
    loader.style.display = 'flex';
}

// Hide loading spinner
function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// API error handler
function handleApiError(error) {
    hideLoader();
    console.error('API Error:', error);
    if (error.response && error.response.status === 401) {
        window.location.href = '/login';
    } else {
        alert('An error occurred. Please try again.');
    }
}

// ==================== HOST MODAL FUNCTIONS ====================

// Open host modal
function openHostModal() {
    const modal = document.getElementById('host-modal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

// Close host modal
function closeHostModal() {
    const modal = document.getElementById('host-modal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

// Redirect to host registration
function redirectToHostRegister() {
    closeHostModal();
    window.location.href = '/host_register';
}

// Close modal when clicking outside
document.addEventListener('click', function(event) {
    const modal = document.getElementById('host-modal');
    if (modal && event.target === modal) {
        closeHostModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeHostModal();
    }
});

console.log('SmartStay JavaScript loaded successfully!');