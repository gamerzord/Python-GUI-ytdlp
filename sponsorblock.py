from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit, QLabel


# SponsorBlock categories and their descriptions
SPONSORBLOCK_CATEGORIES = {
    'sponsor': 'Sponsor - Paid promotion segments',
    'intro': 'Intro - Introductions or opening animations',
    'outro': 'Outro - End credits or closing animations', 
    'selfpromo': 'Self Promotion - Creator promoting their own content',
    'preview': 'Preview - Previews or recaps of the video',
    'filler': 'Filler - Tangential content or unnecessary filler',
    'interaction': 'Interaction - Requests for likes, subscriptions, etc.',
    'music_offtopic': 'Music/Off-topic - Non-music videos with music sections'
}

DEFAULT_CATEGORIES = "sponsor,selfpromo"


def create_sponsorblock_group() -> QGroupBox:
    """Create SponsorBlock configuration group widget"""
    sponsor_group = QGroupBox("SponsorBlock")
    sponsor_layout = QVBoxLayout()
    sponsor_group.setLayout(sponsor_layout)
    
    # Enable SponsorBlock checkbox
    sponsorblock_cb = QCheckBox("Remove sponsored segments")
    sponsorblock_cb.setObjectName("sponsorblock_cb")  # For findChild lookup
    sponsor_layout.addWidget(sponsorblock_cb)
    
    # Categories configuration
    sponsor_options_layout = QHBoxLayout()
    sponsor_options_layout.addWidget(QLabel("Categories:"))
    
    sponsor_categories_input = QLineEdit()
    sponsor_categories_input.setObjectName("sponsor_categories_input")  # For findChild lookup
    sponsor_categories_input.setPlaceholderText("sponsor,intro,outro,selfpromo,preview,filler,interaction,music_offtopic")
    sponsor_categories_input.setText(DEFAULT_CATEGORIES)
    sponsor_categories_input.setToolTip("Comma-separated list of SponsorBlock categories to remove")
    sponsor_options_layout.addWidget(sponsor_categories_input)
    
    sponsor_layout.addLayout(sponsor_options_layout)
    
    # Add description
    description_label = QLabel("Remove segments automatically marked by the SponsorBlock community")
    description_label.setStyleSheet("color: #666666; font-size: 10px;")
    sponsor_layout.addWidget(description_label)
    
    return sponsor_group


def get_category_description(category: str) -> str:
    """Get description for a SponsorBlock category"""
    return SPONSORBLOCK_CATEGORIES.get(category, f"Unknown category: {category}")


def validate_categories(categories_str: str) -> tuple[bool, str]:
    """Validate SponsorBlock categories string"""
    if not categories_str.strip():
        return False, "Categories cannot be empty"
    
    categories = [cat.strip() for cat in categories_str.split(',')]
    invalid_categories = []
    
    for category in categories:
        if category and category not in SPONSORBLOCK_CATEGORIES:
            invalid_categories.append(category)
    
    if invalid_categories:
        return False, f"Invalid categories: {', '.join(invalid_categories)}"
    
    return True, "Valid categories"


def get_default_categories() -> str:
    """Get default SponsorBlock categories"""
    return DEFAULT_CATEGORIES


def get_all_categories() -> list[str]:
    """Get all available SponsorBlock categories"""
    return list(SPONSORBLOCK_CATEGORIES.keys())


def format_categories_for_command(categories_str: str) -> str:
    """Format categories string for yt-dlp command"""
    categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]
    return ','.join(categories)