# MyTrading - Skin Trading Application

## Overview
MyTrading is a comprehensive desktop application for managing CS2, RUST, DOTA2, and TF2 skin trading with advanced features for tracking prices, profits, and creating trading sets.

## Features

### Authentication
- User registration with secure password hashing
- Local SQLite database for user credentials
- Login system with session management

### Trading Table
- Track all purchased and sold items
- Support for multiple games: CS2, RUST, DOTA2, TF2
- Detailed item information with float values and patterns
- Currency conversion (USD, EUR, RUB, UYU, GEL, USDT, USDC, USDP, LTC)
- Commission tracking for each transaction
- Support for multiple marketplaces
- StatTrak and Souvenir item support

### Item Management
- **Item Info**: Display item images, float values, patterns, wear states
- **Buy Section**: Track purchase date, price, currency, fees, marketplace
- **Sell Section**: Track sale date, price, currency, fees, marketplace
- **Profit Calculation**: Automatic profit calculation with percentage display
- **Accessories**: Sticker and charm management

### Sticker Management
- Up to 5 stickers per item
- Sticker type selection (Normal, Glitter, Foil, Holo, Gold, Lenticular, Embroidery, Glossy)
- Price tracking at purchase and sale time
- Support for tournament majors and autographs
- Smart sticker value calculation based on wear state

### Finds Section
- Track potential items to purchase
- Display items in a grid layout with key information
- Track current price vs market price
- Link to marketplace URLs
- Mark as deleted when unavailable

### Sets Section
- Create custom sets of items
- Add multiple items to sets
- Track set prices and descriptions
- Visual set cards with rounded corners (iOS-style)

### Beautiful Trades Section
- Display completed profitable trades
- Show trade details and profit margins
- Visual layout with item images

### Crafts Section
- Track custom skin crafts
- Upload multiple images per craft
- Track pattern, stickers, and prices
- Link to marketplace for purchases

### Trade & Profit Dashboard
- Total profit calculation
- Total invested amount
- Average item price
- Trade cycle calculator
- Currency conversion for profit analysis

### Comparison Tool
- Compare multiple items
- Analyze profit potential
- Calculate expected profit margins
- Get recommendations for best flips

### Settings
- **Theme Selection**: Light, Dark, Black, Purple-Black
- **Default Currency**: Configuration for preferred currency
- **Pattern Management**: Custom pattern and tier configuration
- **Marketplace Management**: Add custom marketplaces
- **Major Tournament Management**: Add new tournament majors

## Supported Games
1. **CS2 (Counter-Strike 2)**
   - Weapons (Knives, Pistols, Rifles, Sniper Rifles, Shotguns, SMGs, Machine Guns)
   - Gloves
   - Agents
   - Music Kits
   - Stickers
   - Patches

2. **RUST**
   - Clothing & Armor
   - Weapons
   - Tools
   - Deployables
   - Miscellaneous items

3. **DOTA2**
   - Hero Cosmetics (Arcana, Persona)
   - Couriers
   - Wards
   - World Customization
   - Interface & Audio

4. **TF2 (Team Fortress 2)**
   - Cosmetics (Hats, Shirts, Pants)
   - War Paints (Decorated Weapons)
   - Taunts
   - Badges

## Currencies Supported
- USD (US Dollar)
- EUR (Euro)
- RUB (Russian Ruble)
- UYU (Uruguayan Peso)
- GEL (Georgian Lari)
- USDT (Tether)
- USDC (USD Coin)
- USDP (Paxos Dollar)
- LTC (Litecoin)

## Marketplaces Supported
- CS.MONEY
- Skinport
- LIS-SKINS
- Tradeit.gg
- CSFloat
- DMarket
- Swap.GG
- Market CSGO
- Steam
- Buff.163
- Youpin
- Buff Market
- UU 163
- Waxpeer
- ShadowPay
- White.market
- FunPay
- playerok
- TG
- Other

## Installation

### Windows (Recommended)
Double-click `run.bat` to start the application. It will:
1. Create a virtual environment (if needed)
2. Install dependencies
3. Launch the application

### Manual Setup
```bash
python -m venv venv
venv\Scripts\activate.bat  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py
```

### Requirements
- Python 3.8+
- PyQt6
- SQLite3 (included with Python)

## Database Schema

The application uses SQLite with the following tables:
- `users` - User accounts with hashed passwords
- `items` - Trading items with full details
- `stickers` - Stickers applied to items
- `charms` - Charms applied to items
- `finds` - Potential items to buy
- `sets` - Custom item sets
- `set_items` - Items within sets
- `crafts` - Custom crafts
- `settings` - User preferences

## Usage

1. **First Launch**: Create an account with username and password
2. **Login**: Enter credentials to access the application
3. **Add Items**: Click "+ Add Item" to start tracking trades
4. **Manage Currency**: Select your preferred currency in the trading table
5. **Change Theme**: Go to Settings and select your preferred theme
6. **Track Trades**: Use the Trading Table to monitor all transactions
7. **Analyze Profits**: Check Trade & Profit for statistics
8. **Find Deals**: Use Finds section to track potential purchases
9. **Create Sets**: Organize items into themed collections
10. **Compare Items**: Use Comparison tool to find best profit opportunities

## Theme Options

1. **Light** - White background with dark text (iOS-style)
2. **Dark** - Dark gray background with light text
3. **Black** - Pure black background with white text
4. **Purple-Black** - Purple-tinted dark background with light text

All themes feature rounded corners (iOS-style) for a modern look.

## File Structure
```
MyTrading/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── run.bat             # Windows launcher
├── run.py              # Cross-platform launcher
├── README.md           # This file
└── trading_app.db      # SQLite database (created on first run)
```

## Portability

The application is fully portable:
- Copy the entire folder to a USB drive
- Run `run.bat` from any Windows PC
- No installation required
- Database is stored locally in the folder

## Security

- Passwords are hashed using SHA-256
- Local database encryption ready
- No external server required
- All data stays on your device

## Features Roadmap

- [ ] API integration with marketplaces for real-time prices
- [ ] Advanced analytics and statistics
- [ ] Export data to CSV/Excel
- [ ] Price history charts
- [ ] Automated profit suggestions
- [ ] Multi-device sync option
- [ ] Mobile companion app
- [ ] Advanced sticker valuation AI
- [ ] Market trend analysis

## Tips for Best Results

1. **Float Values**: Accurate float values are crucial for profit calculation
2. **Sticker Tracking**: Always record sticker wear percentage
3. **Commission Tracking**: Include all fees from marketplaces
4. **Currency Consistency**: Track purchases in original currency
5. **Regular Updates**: Keep item prices current

## Troubleshooting

**Application won't start:**
- Ensure Python 3.8+ is installed
- Run `run.bat` with administrator privileges
- Check if port 5000 is available

**Database errors:**
- Delete `trading_app.db` and restart (creates fresh database)
- Ensure write permissions in application folder

**Display issues:**
- Update graphics drivers
- Try different theme in Settings

## License
Private - All rights reserved

## Support
For issues or feature requests, please contact the developer.

## Version
1.0.0 - Initial Release
