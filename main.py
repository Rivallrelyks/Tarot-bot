import discord
from discord.ext import commands
import random
import os

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Complete 78-card Tarot deck
TAROT_DECK = {
    # Major Arcana
    the fool {suit Major Arcana, number 0, upright New beginnings, innocence, adventure, potential, reversed Recklessness, foolishness, naivety},
    the magician {suit Major Arcana, number I, upright Manifestation, power, creativity, willpower, reversed Manipulation, deception, untapped talents},
    the high priestess {suit Major Arcana, number II, upright Intuition, sacred knowledge, divine feminine, reversed Secrets, disconnection, repressed feelings},
    the empress {suit Major Arcana, number III, upright Femininity, beauty, abundance, creativity, reversed Creative block, dependence, lack of self-care},
    the emperor {suit Major Arcana, number IV, upright Authority, structure, leadership, stability, reversed Tyranny, rigidity, excessive control},
    the hierophant {suit Major Arcana, number V, upright Spiritual wisdom, tradition, teaching, reversed Personal beliefs, freedom, challenging status quo},
    the lovers {suit Major Arcana, number VI, upright Love, relationships, choices, union, reversed Self-love, disharmony, misalignment},
    the chariot {suit Major Arcana, number VII, upright Control, willpower, success, determination, reversed Lack of control, aggression, power struggles},
    strength {suit Major Arcana, number VIII, upright Inner strength, courage, compassion, reversed Self-doubt, weakness, raw emotion},
    the hermit {suit Major Arcana, number IX, upright Soul searching, introspection, inner guidance, reversed Isolation, loneliness, withdrawal},
    wheel of fortune {suit Major Arcana, number X, upright Good luck, karma, life cycles, destiny, reversed Bad luck, lack of control, breaking cycles},
    justice {suit Major Arcana, number XI, upright Justice, fairness, truth, balance, reversed Unfairness, dishonesty, avoiding responsibility},
    the hanged man {suit Major Arcana, number XII, upright Surrender, patience, sacrifice, new perspective, reversed Delays, resistance, playing victim},
    death {suit Major Arcana, number XIII, upright Transformation, endings, new beginnings, reversed Resistance to change, stagnation},
    temperance {suit Major Arcana, number XIV, upright Balance, moderation, patience, healing, reversed Imbalance, excess, hasty decisions},
    the devil {suit Major Arcana, number XV, upright Temptation, materialism, addiction, reversed Breaking free, detachment, reclaiming power},
    the tower {suit Major Arcana, number XVI, upright Sudden change, upheaval, revelation, reversed Fear of change, resisting change},
    the star {suit Major Arcana, number XVII, upright Hope, faith, inspiration, healing, reversed Lack of faith, despair, disconnection},
    the moon {suit Major Arcana, number XVIII, upright Illusion, intuition, dreams, mystery, reversed Release of fear, inner confusion},
    the sun {suit Major Arcana, number XIX, upright Joy, success, positivity, vitality, reversed Inner child, feeling down, unrealistic expectations},
    judgement {suit Major Arcana, number XX, upright Rebirth, awakening, inner calling, reversed Self-doubt, avoiding judgement},
    the world {suit Major Arcana, number XXI, upright Completion, accomplishment, fulfillment, reversed Seeking closure, delays, lack of completion},

    # Cups - Emotions, Love, Spirituality
    ace of cups {suit Cups, number Ace, upright New love, emotional awakening, intuition, reversed Self-love, blocked emotions, spiritual disconnection},
    two of cups {suit Cups, number 2, upright Partnership, love, connection, reversed Break-ups, disharmony, imbalanced relationships},
    three of cups {suit Cups, number 3, upright Friendship, celebration, community, reversed Independence, creative blocks, isolation},
    four of cups {suit Cups, number 4, upright Contemplation, apathy, missed opportunities, reversed Withdrawal, self-absorption, introversion},
    five of cups {suit Cups, number 5, upright Loss, grief, disappointment, reversed Moving on, acceptance, learning from failures},
    six of cups {suit Cups, number 6, upright Nostalgia, childhood memories, innocence, reversed Living in the past, being naive},
    seven of cups {suit Cups, number 7, upright Choices, illusion, fantasy, reversed Alignment, overwhelmed by choices},
    eight of cups {suit Cups, number 8, upright Walking away, searching for truth, reversed Fear of moving on, stagnation},
    nine of cups {suit Cups, number 9, upright Contentment, wish fulfillment, satisfaction, reversed Inner happiness, materialism, dissatisfaction},
    ten of cups {suit Cups, number 10, upright Happy family, harmony, emotional fulfillment, reversed Struggling relationships, disharmony},
    page of cups {suit Cups, number Page, upright Creative opportunities, intuitive messages, reversed Creative blocks, doubting intuition},
    knight of cups {suit Cups, number Knight, upright Romance, charm, following the heart, reversed Unrealistic, jealous, moody},
    queen of cups {suit Cups, number Queen, upright Compassion, intuition, emotional stability, reversed Co-dependency, emotional instability},
    king of cups {suit Cups, number King, upright Emotional balance, compassion, wisdom, reversed Moodiness, emotional manipulation},

    # Pentacles - Material, Money, Career
    ace of pentacles {suit Pentacles, number Ace, upright New opportunity, manifestation, prosperity, reversed Lost opportunity, bad investment},
    two of pentacles {suit Pentacles, number 2, upright Balance, juggling priorities, adaptability, reversed Over-committed, disorganization},
    three of pentacles {suit Pentacles, number 3, upright Teamwork, collaboration, skill building, reversed Lack of teamwork, poor collaboration},
    four of pentacles {suit Pentacles, number 4, upright Security, saving, control, reversed Over-spending, greed, possessiveness},
    five of pentacles {suit Pentacles, number 5, upright Financial hardship, poverty, worry, reversed Recovery, overcoming hardship},
    six of pentacles {suit Pentacles, number 6, upright Generosity, charity, sharing wealth, reversed Self-care, inequality, exploitation},
    seven of pentacles {suit Pentacles, number 7, upright Patience, investment, long-term view, reversed Impatience, lack of long-term vision},
    eight of pentacles {suit Pentacles, number 8, upright Skill development, mastery, dedication, reversed Perfectionism, lack of concentration},
    nine of pentacles {suit Pentacles, number 9, upright Financial independence, luxury, self-sufficiency, reversed Over-investment in work, reckless spending},
    ten of pentacles {suit Pentacles, number 10, upright Wealth, family legacy, long-term success, reversed Financial failure, family disputes},
    page of pentacles {suit Pentacles, number Page, upright Learning, new opportunities, ambition, reversed Lack of progress, procrastination},
    knight of pentacles {suit Pentacles, number Knight, upright Hard work, reliability, patience, reversed Boredom, perfectionism, burned-out},
    queen of pentacles {suit Pentacles, number Queen, upright Nurturing, practical, resourceful, reversed Work-home conflict, jealousy},
    king of pentacles {suit Pentacles, number King, upright Financial success, business leader, abundance, reversed Obsessed with wealth, poor decisions},

    # Swords - Thoughts, Communication, Conflict
    ace of swords {suit Swords, number Ace, upright New ideas, mental clarity, breakthrough, reversed Confusion, miscommunication, chaos},
    two of swords {suit Swords, number 2, upright Difficult decisions, indecision, stalemate, reversed Information overload, emotional detachment},
    three of swords {suit Swords, number 3, upright Heartbreak, sorrow, grief, reversed Releasing pain, forgiveness, healing},
    four of swords {suit Swords, number 4, upright Rest, meditation, recuperation, reversed Exhaustion, burn-out, restlessness},
    five of swords {suit Swords, number 5, upright Conflict, defeat, betrayal, reversed Reconciliation, making amends},
    six of swords {suit Swords, number 6, upright Transition, moving forward, healing, reversed Resistance to change, unfinished business},
    seven of swords {suit Swords, number 7, upright Deception, betrayal, stealth, reversed Confession, getting caught},
    eight of swords {suit Swords, number 8, upright Restriction, trapped, victim mentality, reversed Breaking free, empowerment},
    nine of swords {suit Swords, number 9, upright Anxiety, worry, nightmares, reversed Releasing worry, inner turmoil},
    ten of swords {suit Swords, number 10, upright Rock bottom, betrayal, painful endings, reversed Recovery, healing, surviving disaster},
    page of swords {suit Swords, number Page, upright New ideas, curiosity, communication, reversed All talk no action, haste},
    knight of swords {suit Swords, number Knight, upright Ambition, haste, impulsive action, reversed Restless, impatient, reckless},
    queen of swords {suit Swords, number Queen, upright Independence, clear thinking, direct communication, reversed Harsh judgement, lack of empathy},
    king of swords {suit Swords, number King, upright Mental clarity, authority, truth, reversed Manipulation, abuse of power},

    # Wands - Passion, Creativity, Energy
    ace of wands {suit Wands, number Ace, upright Inspiration, new opportunities, creative spark, reversed Lack of direction, creative blocks},
    two of wands {suit Wands, number 2, upright Planning, personal power, future decisions, reversed Fear of unknown, lack of planning},
    three of wands {suit Wands, number 3, upright Expansion, foresight, leadership, reversed Playing small, lack of foresight},
    four of wands {suit Wands, number 4, upright Celebration, achievement, harmony, reversed Personal celebration, lack of support},
    five of wands {suit Wands, number 5, upright Conflict, competition, struggle, reversed Inner conflict, avoiding tension},
    six of wands {suit Wands, number 6, upright Success, recognition, victory, reversed Private achievement, fall from grace},
    seven of wands {suit Wands, number 7, upright Challenge, defending, perseverance, reversed Exhaustion, giving up},
    eight of wands {suit Wands, number 8, upright Speed, swift action, progress, reversed Delays, frustration, resisting change},
    nine of wands {suit Wands, number 9, upright Resilience, persistence, stamina, reversed Struggle, defensive, stubborn},
    ten of wands {suit Wands, number 10, upright Burden, responsibility, hard work, reversed Delegation, release, working smarter},
    page of wands {suit Wands, number Page, upright Inspiration, enthusiasm, new projects, reversed Self-limiting beliefs, hasty decisions},
    knight of wands {suit Wands, number Knight, upright Passion, adventure, impulsive energy, reversed Haste, scattered energy, reckless},
    queen of wands {suit Wands, number Queen, upright Confidence, independence, determination, reversed Self-confidence issues, social anxiety},
    king of wands {suit Wands, number King, upright Leadership, vision, entrepreneur, reversed Impulsiveness, abuse of power}
}

@bot.event
async def on_ready()
    print(f'{bot.user} is ready! Loaded {len(TAROT_DECK)} cards.')
    print(f'Connected to {len(bot.guilds)} servers')

@bot.command(name='card')
async def card_info(ctx, , card_name str = None)
    if not card_name
        await ctx.send(Please specify a card name! Use `!cards` to see all available cards.)
        return
    
    card_key = card_name.lower().strip()
    
    if card_key not in TAROT_DECK
        await ctx.send(fCard '{card_name}' not found. Use `!cards` to see available cards.)
        return
    
    card = TAROT_DECK[card_key]
    
    response = f{card_key.title()}
{card['suit']} - {card['number']}

Upright {card['upright']}
Reversed {card['reversed']}
    
    await ctx.send(response)

@bot.command(name='draw')
async def draw_card(ctx)
    card_name = random.choice(list(TAROT_DECK.keys()))
    card = TAROT_DECK[card_name]
    is_reversed = random.choice([True, False])
    
    orientation = Reversed if is_reversed else Upright
    meaning = card['reversed'] if is_reversed else card['upright']
    
    response = f{card_name.title()}
{card['suit']} - {card['number']}

{orientation}
{meaning}
    
    await ctx.send(response)

@bot.command(name='spread')
async def three_card_spread(ctx, , spread_type str = past present future)
    spreads = {
        past present future [Past, Present, Future],
        mind body spirit [Mind, Body, Spirit],
        love [You, Partner, Relationship]
    }
    
    spread_key = spread_type.lower()
    if spread_key not in spreads
        available = , .join(spreads.keys())
        await ctx.send(fAvailable spreads {available})
        return
    
    positions = spreads[spread_key]
    drawn_cards = random.sample(list(TAROT_DECK.keys()), 3)
    
    response = f{spread_type.title()} Spreadnn
    
    for i, (position, card_name) in enumerate(zip(positions, drawn_cards), 1)
        card = TAROT_DECK[card_name]
        is_reversed = random.choice([True, False])
        meaning = card['reversed'] if is_reversed else card['upright']
        orientation = if is_reversed else
        
        response += f{i}. {position} {card_name.title()} {orientation}n{meaning}nn
    
    await ctx.send(response)

@bot.command(name='cards')
async def list_cards(ctx, suit str = None)
    if suit
        suit_mapping = {major Major Arcana, cups Cups, pentacles Pentacles, swords Swords, wands Wands}
        if suit.lower() not in suit_mapping
            await ctx.send(Available suits major, cups, pentacles, swords, wands)
            return
        
        target_suit = suit_mapping[suit.lower()]
        filtered_cards = [name for name, card in TAROT_DECK.items() if card['suit'] == target_suit]
        
        response = f{target_suit} ({len(filtered_cards)} cards)n
        response += n.join([f {name.title()} for name in filtered_cards])
    else
        response = fComplete Tarot Deck ({len(TAROT_DECK)} cards)nn
        for suit_name in [Major Arcana, Cups, Pentacles, Swords, Wands]
            count = len([card for card in TAROT_DECK.values() if card['suit'] == suit_name])
            response += f{suit_name} {count} cardsn
        response += nUse `!cards [suit]` to see specific suit
    
    await ctx.send(response)

@bot.command(name='help')
async def help_command(ctx)
    help_text = Tarot Bot Commands

`!card [name]` - Get card info
`!draw` - Draw random card
`!spread [type]` - 3-card spread
`!cards [suit]` - List cards
`!help` - This message

Spreads past present future, mind body spirit, love
    
    await ctx.send(help_text)

# Keep the bot alive for Railway
@bot.event 
async def on_error(event, args, kwargs)
    print(f'An error occurred {event}')

# Start the bot
if __name__ == __main__
    # Get token from environment variable (Railway style)
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN
        print(ERROR DISCORD_TOKEN environment variable not found!)
        print(Please set your Discord bot token in Railway environment variables.)
        exit(1)
    
    try
        bot.run(TOKEN)
    except Exception as e
        print(fFailed to start bot {e})
        exit(1)


