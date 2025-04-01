package store;
@WebListener
public class StoreListener implements ServletContextListener, HttpSessionListener {
public StoreListener() {
}
public void sessionCreated(HttpSessionEvent event)  {
event.getSession().setAttribute(ShoppingCart.SC_NAME, new ShoppingCart());
}
public void sessionDestroyed(HttpSessionEvent event)  {
event.getSession().removeAttribute(ShoppingCart.SC_NAME);
}
public void contextDestroyed(ServletContextEvent event)  {
}
public void contextInitialized(ServletContextEvent event)  {
event.getServletContext().setAttribute(ProductCatalog.PC_NAME, new ProductCatalog());
}
}