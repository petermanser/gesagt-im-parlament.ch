package ch.makeopendata.scraper
import org.htmlcleaner.TagNode
import java.io.FileWriter
import java.io.PrintWriter
import org.htmlcleaner.HtmlCleaner

class Politician(
  val id: Int,
  val party: String) {
  def print {
    println("==============================")
    println("Id: " + id)
    println("Party: " + party)
    println("==============================")
  }
}

object Politician {

  def apply(id: Int): Option[Politician] = {
    val url = "http://www.parlament.ch/d/suche/seiten/biografie.aspx?biografie_id=" + id
    try {
      val website = io.Source.fromURL(url, "UTF-8").mkString
      if (!website.contains("Es wurde kein Parlamentarier mit dieser ID gefunden.")) {
        val cleaner = new HtmlCleaner
        val node = cleaner.clean(website)
        val party = extractParty(node)
        Some(new Politician(id, party))
      } else {
        println(id + "not assigned to a politician")
        None
      }
    } catch {
      case e: Throwable => {
        println("Failed to load url: " + url + " if this is due to connectivity issues, please resume @ id " + id)
        e.printStackTrace
        None
      }
    }
  }

  def reportError(text: String) {
    val fileWriter = new FileWriter("failures-pol.txt", true)
    val printWriter = new PrintWriter(fileWriter)
    printWriter.println(text)
    fileWriter.close
  }

  def extractParty(website: TagNode): String = {
    var partyLink = ""
    val nodes = website.evaluateXPath("//*[@id='content']/div/div/div[2]/ul[2]//li/a/@href").toList
    if (!nodes.isEmpty) {
      nodes foreach {
        link =>
          {
            val castLink = link.asInstanceOf[String]
            if (!castLink.startsWith("http://www.parlament.ch")) {
              partyLink = castLink
            }
          }
      }
    } else {
      val message = "Extraction failed: " + website
      reportError(message)
    }
    partyLink
  }

}