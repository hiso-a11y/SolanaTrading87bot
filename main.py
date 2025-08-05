    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button clicks - FIXED VERSION"""
        query = update.callback_query
        await query.answer()  # Acknowledge the button press
        
        # Create a fake update object for command handlers
        fake_update = Update(
            update_id=update.update_id,
            message=query.message,
            effective_user=update.effective_user,
            effective_chat=update.effective_chat,
            callback_query=query
        )
        
        try:
            if query.data == "balance":
                await self.balance_command(fake_update, context)
            elif query.data == "snipe":
                await self.snipe_command(fake_update, context)
            elif query.data == "status":
                await self.status_command(fake_update, context)
            elif query.data == "help":
                await self.help_command(fake_update, context)
            elif query.data == "stop_snipe":
                user_id = update.effective_user.id
                if user_id in self.trading.active_sessions:
                    session = self.trading.active_sessions.pop(user_id)
                    duration = datetime.utcnow() - session['started_at']
                    await query.edit_message_text(
                        f"⏹️ **Sniping Stopped**\n\n"
                        f"**Session Summary:**\n"
                        f"• Duration: {str(duration).split('.')[0]}\n"
                        f"• Trades: {session['trades_executed']}\n"
                        f"• Profit: {session['total_profit']:+.6f} SOL",
                        parse_mode='Markdown'
                    )
                else:
                    await query.edit_message_text("❌ No active session found.")
            else:
                await query.edit_message_text("⚙️ Feature coming soon!")
                
        except Exception as e:
            logger.error(f"Button handler error: {e}")
            await query.edit_message_text("❌ Button error. Try using commands directly.")
