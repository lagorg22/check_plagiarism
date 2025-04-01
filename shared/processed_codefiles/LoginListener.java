package login;
@WebListener
public class LoginListener implements ServletContextListener {
public LoginListener() {
}
public void contextDestroyed(ServletContextEvent event)  {
}
public void contextInitialized(ServletContextEvent event)  {
AccountManager am = new AccountManager();
ServletContext sc = event.getServletContext();
sc.setAttribute(AccountManager.AM_NAME, am);
}
}